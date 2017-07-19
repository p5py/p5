from setuptools import setup, find_packages

from os import path

setup(
    name='p5',
    version='0.1.0dev4',
    license="GPLv3",
    description="p5 is a python package based on the core ideas of Processing.",
    author="Abhik Pal",
    author_email='theabhikpal@gmail.com',
    url='https://p5py.github.io',
    packages=find_packages(exclude=['tools']),
    install_requires=['pyglet'],
)
