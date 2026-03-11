
import os
import re 
import sys
import json
import logging
import argparse
import importlib.metadata
import opensafer
import subprocess
from collections import deque

LOGGER:logging = logging.getLogger(__name__)

def package_tree_as_list (packages:"list[dict[str, typing.Any]]") -> "list[dict[str, typing.Any]]":

  """階層構造になっているパッケージ情報をひとつのリストに列挙します。

  Parameters
  ----------
  packages : list[dict[str, typing.Any]]
    列挙対象となるパッケージのリストです。

  Returns
  -------
  list[dict[str, typing.Any]]
    階層構造に存在するすべてのパッケージが列挙されたリストです。
  """

  result = []
  for package in packages:
    deq = deque([package])
    while deq:
      p = deq.pop()
      deq.extend(reversed(p.get("_dependencies", [])))
      result.append(p)
  return result

def unique_list (source:"list[typing.Any]") -> "list[typing.Any]":

  """一意の値だけを持つリストを作成します。

  Parameters
  ----------
  source : list[typing.Any]
    操作対象となるリストです。
    本関数は副作用を持たないため、本引数のリストに変化は起こりません。

  Returns
  -------
  list[typing.Any]
    一意の値だけを持つリストです。
  """

  result = []
  for index, item in enumerate(source):
    if item not in source[:index]:
      result.append(item)
  return result

def find_license (package:"dict[str, typing.Any]") -> "typing.Generator[tuple[pathlib.Path|None, str], None, None]":

  """パッケージ情報からライセンス情報を取得します。

  Parameters
  ----------
  package : dict[str, typing.Any]
    ライセンス情報を取得する対象となるパッケージ情報です。

  Returns
  -------
  typing.Generator[tuple[pathlib.Path|None, str], None, None]
    パッケージ情報から取得することができたライセンス情報の一覧です。
    これはライセンスファイルのパス名・その内容の組の集合となっています。
    パッケージ情報の内容によっては、パス名は `None` となることがあります。
  """

  license_file = package.get("license_file", "")
  if license_file:
    try:
      package_files = importlib.metadata.files(package["name"])
      for file in package_files:
        if file.name == license_file:
          yield file, file.read_text(encoding="utf-8")
      return
    except ModuleNotFoundError:

      LOGGER.error("Could not load module: {:s}({:s})".format(package["name"], dist_name)) #log.

  license = package.get("license", "")
  if license:
    yield None, license

    LOGGER.info("Found a license from metadata, but it may be incomplete as license, so please check your self it: {:s}".format(package["name"]))

def dump_header_texts (texts:list[str], *, file:"io.TextIOBase", separator:str):

  """各ライセンスのヘッダ部分を出力します。
  """

  separator_len = max((len(line) for line in texts), default=0)
  separator_text = (separator * separator_len)[:separator_len]
  print(separator_text, file=file)
  for line in texts:
    print(line, file=file)
  print(separator_text, file=file)

def dump_license (packages:"list[dict[str, typing.Any]]", *, file:"io.TextIOBase", separator:str):

  """複数のパッケージのライセンスを出力します。
  """

  failed_packages = list()
  for package in packages:
    found_licenses = list(find_license(package))
    if found_licenses:
      for license_file, license in find_license(package):
        headertexts = []
        if license_file:
          headertexts.append("License file {!r} of {:s}".format(license_file.name, package["name"]))
        else:
          headertexts.append("License text of {:s}".format(package["name"]))
        project_url = package.get("project_url", [])
        if project_url:
          headertexts.append("")
          headertexts.extend(project_url)
        dump_header_texts(headertexts, file=file, separator=separator)
        print(file=file)
        print(license.strip(), file=file)
        print(file=file)
    else:
      failed_packages.append(package)
  for package in failed_packages:

    LOGGER.info("Could not find license info into package: {:s}".format(package["name"])) #log.

def get_pip_info_tree (packages:list[str]) -> "list[dict[str, typing.Any]]":

  """pip-tree コマンドから指定パッケージの依存情報を取得します。
  """

  process = subprocess.run(["pip-tree", "--json"] + packages, shell=True, text=True, stdout=subprocess.PIPE, check=True)
  return json.loads(process.stdout)

def main ():
  parser = argparse.ArgumentParser(description="Dump all licenses of installed package by pip.")
  parser.add_argument("packages", nargs="*", help="Package names for dump.")
  parser.add_argument("-o", "--output-file", type=str, default="", help="Path of output file. (default is stdout).")
  parser.add_argument("--debug", action="store_true", help="If it enabled, this will print out debug log.")
  parser.add_argument("--ignore-packages", nargs="*", help="List of ignore packages.")
  args = parser.parse_args()
  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  packages = get_pip_info_tree(args.packages)
  packages = unique_list(package_tree_as_list(packages))
  packages = [pkg for pkg in packages if pkg["name"] not in args.ignore_packages] #Delete ignored packages.
  if args.output_file:
    stream = opensafer.open_safer(args.output_file, "w", encoding="utf-8")
  else:
    stream = os.fdopen(os.dup(sys.stdout.fileno()), "w", encoding="utf-8")
  with stream as unwrapped_stream:
    dump_license(packages, file=unwrapped_stream, separator="=")

if __name__ == "__main__":
  main()
