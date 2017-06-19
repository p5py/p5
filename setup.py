from distutils.core import setup

setup(
    name='p5',
    version='0.1.0dev1',
    description="p5 is a python package based on the core ideas of Processing.",
    license="GPLv3",
    author="Abhik Pal",
    author_email='theabhikpal@gmail.com',
    url='https://p5py.github.io',
    packages=[
        'p5', 'p5.core','p5.opengl', 'p5.pmath', 'p5.sketch', 'p5.tmp'
    ],
)
