=====
Shape
=====

.. automodule:: p5
   :noindex:

PShape
======

.. autoclass:: PShape
   :members:


2D Primitives
=============

point()
-------

.. autofunction:: point


line()
------

.. function:: line(x1, y1, x2, y2)
   :noindex:
.. function:: line(x1, y1, z1, x2, y2, z2)
   :noindex:
.. autofunction:: line(p1, p2)


ellipse()
---------

.. function:: ellipse(a, b, c, d, mode=None)
   :noindex:
.. autofunction:: ellipse(coordinate, *args, mode=None)


circle()
--------

.. function:: circle(x, y, radius, mode=None)
   :noindex:
.. autofunction:: circle(coordinate, radius, mode=None)


arc()
-----

.. function:: arc(x, y, width, height, start_angle, stop_angle, mode=None, ellipse_mode=None)
   :noindex:
.. autofunction:: arc(coordinate, width, height, start_angle, stop_angle, mode=None, ellipse_mode=None)


triangle()
----------

.. function:: triangle(x1, y1, x2, y2, x3, y3)
   :noindex:
.. autofunction:: triangle(p1, p2, p3)


quad()
------

.. function:: quad(x1, y1, x2, y2, x3, y3, x4, y4)
   :noindex:
.. autofunction:: quad(p1, p2, p3, p4)


rect()
------

.. function:: rect(x, y, w, h)
   :noindex:
.. autofunction:: rect(coordinate, *args, mode=None)


square()
--------

.. function:: square(x, y, side_length)
   :noindex:
.. autofunction:: square(coordinate, side_length, mode=None)


Curves
======

bezier()
--------

.. autofunction:: bezier


bezier_detail()
---------------

.. autofunction:: bezier_detail


bezier_point()
--------------

.. autofunction:: bezier_point


bezier_tangent()
----------------

.. autofunction:: bezier_tangent


curve()
-------

.. autofunction:: curve


curve_detail()
--------------

.. autofunction:: curve_detail


curve_point()
-------------

.. autofunction:: curve_point


curve_tangent()
---------------

.. autofunction:: curve_tangent


curve_tightness()
-----------------

.. autofunction:: curve_tightness


Attributes
==========

ellipse_mode()
--------------

.. autofunction:: ellipse_mode


rect_mode()
-----------

.. autofunction:: rect_mode


3D Primitives
=============

box()
-----------

.. autofunction:: box


plane()
-----------

.. autofunction:: plane


sphere()
-----------

.. autofunction:: sphere


ellipsoid()
-----------

.. autofunction:: ellipsoid


cylinder()
-----------

.. autofunction:: cylinder


cone()
-----------

.. autofunction:: cone


torus()
-----------

.. autofunction:: torus



Vertex
======


begin_shape()
-------------

.. autofunction:: begin_shape


end_shape()
-----------

.. autofunction:: end_shape


begin_contour()
---------------

.. autofunction:: begin_contour


end_contour()
-------------

.. autofunction:: end_contour


vertex()
--------

.. autofunction:: vertex


curve_vertex()
--------------

.. autofunction:: curve_vertex


bezier_vertex()
---------------

.. autofunction:: bezier_vertex


quadratic_vertex()
------------------

.. autofunction:: quadratic_vertex