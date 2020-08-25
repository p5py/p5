=====
Image
=====

.. module:: p5
   :noindex:

PImage
======

.. autoclass:: PImage
   :members:
   :special-members:


Loading and displaying
======================

image()
-------

.. function:: image(img, x, y)
   :noindex:
.. function:: image(img, x, y, w, h)
   :noindex:
.. autofunction:: image(img, location, size=None)

image_mode()
------------

.. autofunction:: image_mode

load_image()
------------

.. autofunction:: load_image

tint()
------

.. autofunction:: tint
   :noindex:

no_tint()
---------

.. autofunction:: no_tint
   :noindex:

Pixels
======

load_pixels()
-------------

.. autofunction:: load_pixels

pixels
------

A :class:`p5.PImage` containing the values for all the pixels in the
display window. The size of the image is that of the main rendering
window, width × height. This image is only available within the
:meth:`p5.load_pixels` context manager and set to ``None`` otherwise.

.. code:: python

   with load_pixels():
       # code manipulating the ``pixels`` object

Subsequent changes to this image object aren't reflected until
:meth:`p5.load_pixels` is called again. The contents of the display
are updated as soon as program execution leaves the context manager.

