.. image :: https://github.com/p5py/p5/raw/develop/docs/_static/processing-header-thin.png
    :width: 100%
    :align: center
    :alt: ---

p5
===

p5 is a Python library that provides high level drawing functionality
to help you quickly create simulations and interactive art using
Python. It combines the core ideas of `Processing
<https://processing.org/>`_ — learning to code in a visual context —
with Python's readability to make programming more accessible to
beginners, educators, and artists.

Example
-------

.. image:: https://github.com/p5py/p5/blob/develop/docs/_static/readme.gif

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

Installation
------------

p5 requires Python 3 to run. Once you have the correct version of
Python installed, you can run:

.. code:: bash

   $ pip install numpy
   $ pip install p5 --user

to install p5.


Features Roadmap
----------------

Our end goal is to create a Processing-like API for Python. However,
instead of being a strict port of the original Processing API, we will
also try to extend it and use Python's goodness whenever we can.

For now, though, we plan to focus on the following features:

#. Support most 2D drawing primitives and related utility functions
   from the Processing API (as of the latest release, this is almost
   done).

#. Support other parts of the Processing API: images, fonts, etc.

#. Port relevant tutorials and reference material from Processing's
   documentation.

#. Support live coding of sketches in the Python REPL (here's a
   `screencast <https://p5py.github.io/videos/p5-repl-demo.webm>`_ from
   an earlier prototype).


License
-------

p5 is licensed under the GPLv3. See `LICENSE <LICENSE>`_ for more
details. p5 also includes the following components from other open
source projects:

- OpenGL shaders `from the Processing
  <https://github.com/processing/processing/tree/master/core/src/processing/opengl/shaders>`_
  project. Licensed under LGPL v2.1. See `LICENSES/lgpl-2.1.txt
  <LICENSES/lgpl-2.1.txt>`_ for the full license text.

- Code from the `Glumpy <http://glumpy.github.io/>`_ project See
  `LICENSES/glumpy.txt` for the full license text from the Glumpy
  project.

All licenses for these external components are available in the
``LICENSES`` folder.

.. image :: https://github.com/p5py/p5/raw/develop/docs/_static/processing-header-thin.png
    :width: 100%
    :align: center
    :alt: ---
