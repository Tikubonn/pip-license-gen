
import os
import sys
import json
import logging
import argparse
import importlib.metadata
import opensafer
import subprocess
from collections import deque

_LOGGER:"logging.Logger" = logging.getLogger(__name__)

def package_tree_as_list (packages:"list[dict[str, typing.Any]]") -> "list[dict[str, typing.Any]]":

  """階層構造になっているパッケージ情報を一意のリストに列挙します。

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
      if p not in result: #列挙済みでなければ末尾に追加する
        result.append(p)
  return result

def find_licenses (package:"dict[str, typing.Any]") -> "typing.Generator[tuple[pathlib.Path|None, str], None, None]":

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

          _LOGGER.info("Found a license file: file={:s} package={:s}".format(file.as_posix(), package["name"])) #log.

          yield file, file.read_text(encoding="utf-8")
      return
    except ModuleNotFoundError:

      _LOGGER.error("Could not load module: {:s}({:s})".format(package["name"], dist_name)) #log.

  license = package.get("license", "")
  if license:
    yield None, license

    _LOGGER.warning("Found a license from metadata, but it may be incomplete as license, so please check your self it: {:s}".format(package["name"]))

def dump_header_texts (texts:list[str], *, file:"io.TextIOBase", separator:str):

  """各ライセンスのヘッダ部分を出力します。
  """

  separator_len = max((len(line) for line in texts), default=0)
  separator_text = (separator * separator_len)[:separator_len]
  print(separator_text, file=file)
  for line in texts:
    print(line, file=file)
  print(separator_text, file=file)

def dump_licenses_as_text (packages:"list[dict[str, typing.Any]]", *, file:"io.TextIOBase", separator:str):

  """複数のパッケージのライセンスを出力します。
  """

  for package in packages:
    found_licenses = list(find_licenses(package))
    if found_licenses:
      for license_file, license in found_licenses:
        header_texts = []
        if license_file:
          header_texts.append("License file {:s} of {:s}".format(license_file.name, package["name"]))
        else:
          header_texts.append("License text of {:s}".format(package["name"]))
        project_url = package.get("project_url", [])
        if project_url:
          header_texts.append("")
          header_texts.extend(project_url)
        dump_header_texts(header_texts, file=file, separator=separator)
        print(file=file)
        print(license.strip("\n"), file=file)
        print(file=file)
    else:

      _LOGGER.warning("Could not find license from package: {:s}".format(package["name"])) #log.

def dump_licenses_as_json (packages:"list[dict[str, typing.Any]]", file:"io.TextIOBase"):
  result = []
  for package in packages:
    found_licenses = list(find_licenses(package))
    if found_licenses:
      for license_file, license in found_licenses:
        pkg = package.copy()
        pkg.setdefault("_found_licenses", [])
        pkg["_found_licenses"].append({
          "file": license_file.as_posix(),
          "text": license.strip("\n")
        })
        result.append(pkg)
    else:

      _LOGGER.warning("Could not find license from package: {:s}".format(package["name"])) #log.

  json.dump(result, file, indent=2)

def get_pip_info_tree (packages:list[str]) -> "list[dict[str, typing.Any]]":

  """pip-tree コマンドから指定パッケージの依存情報を取得します。
  """

  process = subprocess.run(["pip-tree", "--json"] + packages, shell=True, text=True, stdout=subprocess.PIPE, check=True)
  return json.loads(process.stdout)

def main ():
  parser = argparse.ArgumentParser(description="Dump all licenses of installed package by pip.")
  parser.add_argument("packages", nargs="*", default=[], help="Package names for dump.")
  parser.add_argument("-o", "--output-file", type=str, default="", help="Path of output file. (default is stdout).")
  parser.add_argument("--debug", action="store_true", help="If it enabled, this will print out debug log.")
  parser.add_argument("--ignore-packages", nargs="*", default=[], help="List of ignore packages.")
  parser.add_argument("--format", type=str, choices=["text", "json"], default="text")
  args = parser.parse_args()
  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  packages = get_pip_info_tree(args.packages)
  packages = package_tree_as_list(packages)
  packages = [pkg for pkg in packages if pkg["name"] not in args.ignore_packages] #--ignore-packages 指定があれば除外する
  if args.output_file:
    stream = opensafer.open_safer(args.output_file, "w", encoding="utf-8")
  else:
    stream = os.fdopen(os.dup(sys.stdout.fileno()), "w", encoding="utf-8") #dup stdout.
  with stream as unwrapped_stream:
    match args.format:
      case "text":
        dump_licenses_as_text(packages, file=unwrapped_stream, separator="=")
      case "json":
        dump_licenses_as_json(packages, file=unwrapped_stream)
      case _:
        raise ValueError("Given an unknown format: {!r}".format(args.format))

if __name__ == "__main__":
  main()
