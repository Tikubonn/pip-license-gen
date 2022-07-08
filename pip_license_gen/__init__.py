
import os 
import sys 
import json 
import requests
import subprocess 
from pathlib import Path 
from argparse import ArgumentParser
from collections import deque

def open_output_file (path, *args, **kwargs):
  if path:
    return open(path, *args, **kwargs)
  else:
    fd = os.dup(sys.stdout.fileno())
    return os.fdopen(fd, *args, **kwargs)

def list_package_info (packageinfos, *, ignorepackages=[]):
  pkginfos = list()
  for packageinfo in packageinfos:
    if packageinfo["Name"] not in ignorepackages:
      pkginfodeq = deque([packageinfo])
      while pkginfodeq:
        pkginfo = pkginfodeq.pop()
        pkginfodeq.extend(reversed(pkginfo.get("Dependencies", [])))
        pkginfos.append(pkginfo)
  return pkginfos

def unique_list (sequencial):
  newsequence = list()
  for index, value in enumerate(sequencial):
    if value not in sequencial[:index]:
      newsequence.append(value)
  return newsequence

def find_license_files (packageinfo, *, patterns):
  files = list()
  for pattern in patterns:
    packagedir = Path(packageinfo["Location"]).joinpath("{:s}-{:s}.dist-info".format(packageinfo["Name"].replace("-", "_"), packageinfo["Version"]))
    files += [path for path in packagedir.glob(pattern) if path.is_file()]
  return files 

def find_licenses (packageinfo, *, patterns):
  if "Location" in packageinfo and "Name" in packageinfo and "Version" in packageinfo:
    locationandtexts = list()
    for pattern in patterns:
      packagedir = Path(packageinfo["Location"]).joinpath("{:s}-{:s}.dist-info".format(packageinfo["Name"].replace("-", "_"), packageinfo["Version"]))
      for file in packagedir.glob(pattern):
        if file.is_file():
          with open(file, "r", encoding="utf-8") as stream:
            locationandtexts.append((file.name, stream.read()))
    return locationandtexts
  elif "LicenseURLs" in packageinfo:
    locationandtexts = list()
    for url in packageinfo["LicenseURLs"]:
      req = requests.get(url)
      locationandtexts.append((url, req.text))
    return locationandtexts
  else:
    return []

def dump_license (packageinfos, *, licensefilepatterns, separatorchar="=", outputfile=sys.stdout, errorfile=sys.stderr):
  skippedpackages = list()
  for packageinfo in packageinfos:
    locationandlicenses = find_licenses(packageinfo, patterns=licensefilepatterns)
    if locationandlicenses:
      for location, license in locationandlicenses:
        headertexts = list()
        headertexts.append("License file {!r} of {:s}.".format(location, packageinfo["Name"]))
        if "Home-page" in packageinfo:
          headertexts.append(packageinfo["Home-page"])
        separatortext = separatorchar * max((len(text) for text in headertexts))
        print(separatortext, file=outputfile)
        for text in headertexts:
          print(text, file=outputfile)
        print(separatortext, file=outputfile)
        print(file=outputfile)
        print(license.strip("\n"), file=outputfile)
        print(file=outputfile)
    else:
      skippedpackages.append(packageinfo) #error 
  for packageinfo in skippedpackages:
    print("Could not find the license file in package {:s}. Please add it yourself.".format(packageinfo["Name"]), file=errorfile) #error 

def get_pip_info_tree (packages=[]):
  process = subprocess.run(["pip-tree"] + packages + ["--json"], shell=True, text=True, stdout=subprocess.PIPE, check=True)
  return json.loads(process.stdout)

def get_pip_info_tree_from_files (files=[]):
  packageinfos = list()
  for file in files:
    with open(file, "r", encoding="utf-8") as stream:
      packageinfos.extend(json.load(stream))
  return packageinfos

def main ():
  parser = ArgumentParser(description="Dump all licenses of installed package by pip.")
  parser.add_argument("packages", nargs="*", help="Package names for dump.")
  parser.add_argument("--from-json", nargs="+", help="Dump all package licenses from JSON file.")
  parser.add_argument("--license-file-pattern", nargs="+", default=["LICENSE*", "COPYRIGHT*", "COPYING*"], help="Pattern of license file name. default are \"LICENSE*\", \"COPYRIGHT*\" and \"COPYING*\".")
  parser.add_argument("-i", "--ignore-package", nargs="+", help="Package names for ignore.")
  parser.add_argument("-o", "--output-file", type=Path, help="Path of output file. (default is stdout).")
  parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1.0")
  args = parser.parse_args()
  if args.from_json:
    packageinfos = get_pip_info_tree_from_files(args.from_json)
  else:
    packageinfos = get_pip_info_tree(args.packages)
  pkginfos = unique_list(list_package_info(packageinfos))
  with open_output_file(args.output_file, "w", encoding="utf-8") as stream:
    dump_license(pkginfos, licensefilepatterns=args.license_file_pattern, outputfile=stream)

if __name__ == "__main__":
  main()
