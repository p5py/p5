p5
===


|License| |Version| |Slack|  |SanityTests| |Pylint| |Pytest|

.. |License| image:: https://img.shields.io/pypi/l/p5?color=light-green
.. |Version| image:: https://img.shields.io/pypi/v/p5?color=blue
.. |Slack| image:: https://img.shields.io/badge/Slack-Join!-yellow  
           :target: https://join.slack.com/t/p5py/shared_invite/zt-g9uo4vph-dUVltiE1ixvmjFTCyRlzpQ
.. |SanityTests| image:: https://github.com/p5py/p5/actions/workflows/sanityTesting.yml/badge.svg
.. |Pylint| image:: https://github.com/p5py/p5/actions/workflows/pylint.yml/badge.svg
.. |Pytest| image:: https://github.com/p5py/p5/actions/workflows/pytest.yml/badge.svg

p5 is a Python library that provides high level drawing functionality
to help you quickly create simulations and interactive art using
Python. It combines the core ideas of `Processing
<https://processing.org/>`_ — learning to code in a visual context —
with Python's readability to make programming more accessible to
beginners, educators, and artists.

To report a bug / make a feature request use the `issues page <https://github.com/p5py/p5/issues>`_ in this repository. You can also use the `discourse platform
<https://discourse.processing.org/c/p5py/27>`_  to ask/discuss anything related to p5py. 

Example
-------

.. image:: https://github.com/p5py/p5/raw/develop/docs/_static/readme.gif

p5 programs are called "sketches" and are run as any other Python
program. The sketch above, for instance, draws a circle at the mouse
location that gets a random reddish color when the mouse is pressed
and is white otherwise; the size of the circle is chosen randomly. The
Python code for the sketch looks like:

.. code:: python

   from p5 import *

   def setup():
       size(640, 360)
       no_stroke()
       background(204)

   def draw():
       if mouse_is_pressed:
           fill(random_uniform(255), random_uniform(127), random_uniform(51), 127)
       else:
           fill(255, 15)

       circle_size = random_uniform(low=10, high=80)

       circle((mouse_x, mouse_y), circle_size)

   def key_pressed(event):
       background(204)

   run()

Documentation
-------------
The p5py documentation can be found here `p5 documentation
<http://p5.readthedocs.io>`_

Installation
------------

Take a look at the installation steps here in the `p5 installation page
<http://p5.readthedocs.io/en/latest/install.html>`_

Contributing
------------
We welcome contributions from anyone, even if you are new to open source. You can start by fixing the existing `issues <https://github.com/p5py/p5/issues>`_ in p5py. In case you need any help or support from the p5py development community, you can join our `slack group <https://join.slack.com/t/p5py/shared_invite/zt-g9uo4vph-dUVltiE1ixvmjFTCyRlzpQ>`_. 

License
-------

p5 is licensed under the GPLv3. See `LICENSE <LICENSE>`_ for more
details. p5 also includes the following components from other open
source projects:

- OpenGL shaders `from the Processing
  <https://github.com/processing/processing/tree/master/core/src/processing/opengl/shaders>`_
  project. Licensed under LGPL v2.1. See `LICENSES/lgpl-2.1.txt
  <LICENSES/lgpl-2.1.txt>`_ for the full license text.

All licenses for these external components are available in the
``LICENSES`` folder.
