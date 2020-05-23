===========
Environment
===========

.. automodule:: p5
   :noindex:

size()
======

.. autofunction:: size


title()
=======

.. autofunction:: title


height, width
=============

Global integers that store the current width and height of the sketch
window.

..
   cursor()
   ========

   .. autofunction:: cursor


   no_cursor()
   ===========

   .. autofunction:: no_cursor


   focused
   =======

   Global boolean that confirms if the sketch is "focused" i.e., if the
   program is active and will accept mouse or keyboard input, this
   variable is `True` and `False` otherwise.

frame_count
===========

Global integer that keeps track of the current frame number of the
sketch i.e., the number of frames that have been drawn since the
sketch was started.

frame_rate
==========

Global integer variable that keeps track of the current frame rate of
the sketch. The frame rate can only be set when the sketch is run by
passing in the optional :code:`frame_rate` keyword argument to the
:code:`run()` function. See the :code:`run()` function's reference
page for details.
