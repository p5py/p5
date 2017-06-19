from distutils.core import setup

setup(
    name='p5',
    version='0.1.0dev1',
    author_email='theabhikpal@gmail.com',
    url='https://p5py.github.io',
    packages=[
        'p5', 'p5.core', 'p5.opengl', 'p5.pmath', 'p5.sketch',
        'p5.tmp',
    ]
)
