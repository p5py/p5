import os
import sys

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

packages = ['p5']

requires = ['pyglet>=1.3.0']

meta_data = {}
with open(os.path.join(here, 'p5', '__version__'), 'r', 'utf-8') as f:
    exec(f.read(meta_data))

with open('README.rst', 'r' 'utf-8') as f:
    readme = f.read()

setup(
    name=meta_data['__title__'],
    version=meta_data['__version__'],
    description=meta_data['__description__'],
    long_description=readme,
    author=meta_data['__author__'],
    url=meta_data['__url__'],
    author_email=meta_data['__author_email__'],
    license=meta_data['__license__'],
    packages=packages,
    package_data={'': ['LICENSE'], },
    package_dir={'p5': 'p5'},
    include_package_data=True,
    install_requires=requires,
)
