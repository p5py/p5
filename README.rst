.. image :: docs/_static/processing-header-thin.png
    :width: 100%
    :align: center
    :alt: ---

p5
===

p5 is a Python package based on the core ideas of `Processing
<https://processing.org>`_. It aims to make programming more
accessible for beginners, artists, and educators by combining Python's
readability with Processing's emphasis on learning to code in a visual
context.

p5 programs are called "sketches" (we borrow this metaphor from
Processing) and can be run as normal Python programs. A typical sketch
often looks like:

.. code:: python

   # Example adapted from "Recursion" Processing example
   
   from p5 import *

   def setup():
       size(640, 360)
       no_stroke()
       no_loop()

   def draw():
       draw_circle(WIDTH/2, 280, 6)

   def draw_circle(x, radius, level):
       fill(126 * level / 4)
       circle(x, HEIGHT/2, radius*2*)
       if level > 1:
           level = level - 1
          draw_circle(x - radius/1, radius/2, level)
          draw_circle(x + radius/1, radius/2, level)
           
When run, this sketch produces:

.. image:: docs/_static/sample_output.png
   :align: center
   :alt: Sample sketch output


p5 is in its early development phase right now and is being
developed as a `project
<https://summerofcode.withgoogle.com/projects/#5809403503575040>`_
under the `Processing Foundation <https://processingfoundation.org/>`_
for `Google Summer of Code 2017
<https://summerofcode.withgoogle.com/>`_. `Manindra Moharana
<http://www.mkmoharana.com/>`_ will be mentoring me (`Abhik Pal
<https://github.com/abhikpal>`_) for the duration of the GSOC.


Features Overview
-----------------

In addition to supporting the Processing API, p5 will also:

#. Try to have as few dependencies as possible (we are only using
   `pyglet <http://pyglet.org>`_ as of now :) .

#. Minimize boilerplate required to get started.

#. Support live coding of sketches in the Python REPL (here's a
   `screencast <https://p5py.github.io/videos/p5-repl-demo.webm>`_ from
   an earlier prototype).

#. Introduce Python's keyword arguments to existing Processing
   functions to make them more intuitive to use.

#. Use context managers to simplify ``begin*()/end*()`` and
   ``push*()/pop*()`` pairs.

   .. code:: python

      # this:

      push_matrix()
      # code
      pop_matrix()

      # becomes:

      with push_matrix():
         # code
         
Setup
-----

p5 is heavily under development right now and once it reaches some
level of stability, we plan to make it available on PyPI. If you would
like to play around with the existing devlopment code, first clone the
repository

.. code:: shell

   git clone https://github.com/p5py/p5

and then install all requirements:

.. code:: shell

   cd p5
   pip install -r requirements.txt

You can now use p5 (as long as you stay in the current folder) like
a python package. If you would like to use p5 from arbitrary
locations on your drive, you can hack the PYTHONPATH environment
variable.

.. code:: shell

   export PYTHONPATH=$PYTHONPATH:/path/to/the/p5-repo

Contributing
------------

If you think you've found a bug, please use the `Issues
<https://github.com/p5py/p5/issues>`_ tab for this repository.

License
-------

p5 is licensed under the GPLv3. See `LICENSE <LICENSE>`_ for more details.

.. image :: docs/_static/processing-header-thin.png
    :width: 100%
    :align: center
    :alt: ---
