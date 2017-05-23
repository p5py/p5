p5py
====

Introduction
------------

p5py is a Python package based on the core ideas of `Processing
<https://processing.org>`_. It aims to make programming easier to
teach (and learn!) by leveraging Python’s syntax and using
Processing’s visual "sketch" metaphor. In addition to supporting the
Processing API, p5py will also:

#. Try to have as few dependencies as possible (we are only using
   `pyglet <http://pyglet.org>`_ as of now :) .

#. Minimize boilerplate required to get started. A sketch will
   typically require only one ``import`` (p5py automatically takes care
   of running the Python file as a Processing sketch.) 

   .. code:: python

     from p5py import *

     def setup():
         size(400, 300)
         background(51)
         no_fill()

     def draw():
         stroke(127)
         ellipse(mouse_x, mouse_y, 50, 50)

     def mouse_pressed():
         background(51)

#. Support live coding of sketches in the Python REPL (here's a
   `screencast <https://abhikpal.github.io/videos/p5py-screencast.webm>`_ from
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

p5py is heavily under development right now and once it reaches some
level of stability, we plan to make it available on PyPI. If you would
like to play around with the existing devlopment code, first clone the
repository

.. code:: shell

   git clone https://github.com/abhikpal/p5py

and then install all requirements:

.. code:: shell

   cd p5py
   pip install -r requirements.txt

You can now use p5py (as long as you stay in the current folder) like
a python package. If you would like to use p5py from arbitrary
locations on your drive, you can hack the PYTHONPATH environment
variable.

.. code:: shell

   export PYTHONPATH=$PYTHONPATH:/path/to/the/p5py-repo

If you think you've found a bug, please use the `Issues
<https://github.com/abhikpal/p5py/issues>`_ tab for this repository.


License
-------

p5py is licensed under the GPLv3. See `LICENSE <LICENSE>`_ for more details
