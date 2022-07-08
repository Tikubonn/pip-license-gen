
from setuptools import setup, find_packages

setup(
  name="pip-license-gen",
  version="0.1.0",
  description="Dump all license of installed package by pip.",
  author="tikubonn",
  author_email="https://twitter.com/tikubonn",
  url="https://github.com/tikubonn/pip-license-gen",
  license="MIT",
  packages=find_packages(),
  install_requires=[
    "requests",
    "pip-tree@git+https://github.com/tikubonn/pip-tree#egg=pip-tree",
  ],
  entry_points={
    "console_scripts": [
      "pip-license-gen = pip_license_gen:main",
    ],
  },
)
