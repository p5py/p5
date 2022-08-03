#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

packages = ["p5"]

with open("requirements.txt", "r", encoding="UTF-8") as f:
    requires = f.read().split("\n")

meta_data = {}

with open(os.path.join(here, "p5", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), meta_data)

with open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name=meta_data["__title__"],
    version=meta_data["__version__"],
    description=meta_data["__description__"],
    long_description=readme,
    long_description_content_type="text/x-rst",
    author=meta_data["__author__"],
    url=meta_data["__url__"],
    author_email=meta_data["__author_email__"],
    license=meta_data["__license__"],
    packages=find_packages(),
    package_data={
        "": ["LICENSE"],
    },
    package_dir={"p5": "p5"},
    include_package_data=True,
    install_requires=requires,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Artistic Software",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
