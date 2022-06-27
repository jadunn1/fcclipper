#!/usr/bin/env python3
import os
from codecs import open
from setuptools import setup, find_packages

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "fcclipper", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

requires = [
    "appdirs~=1.4.4",
    "click~=7.0",
    "pyppeteer~=1.0.2",
    "rich~=12.4.4",
]

setup(
  name=about["__title__"],
  version=about["__version__"],
  url=about["__url__"],
  author=about["__author__"],
  license=about["__license__"],
  packages=find_packages(),
  install_requires=requires,
  description=about["__description__"],
  long_description=readme,
  long_description_content_type="text/markdown",
  entry_points={
    'console_scripts': [
      'fcclipper = fcclipper.__main__:cli',
        ],
    }
)
