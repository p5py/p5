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

.. function:: ellipse(a, b, c, d)
   :noindex:
.. autofunction:: ellipse(coordinate, *args, mode=None)


circle()
--------

.. function:: circle(x, y, radius, mode=None)
   :noindex:
.. autofunction:: circle(coordinate, radius, mode=None)


arc()
-----

.. autofunction:: arc


triangle()
----------

.. autofunction:: triangle


quad()
------

.. autofunction:: quad


rect()
------

.. autofunction:: rect


square()
--------

.. autofunction:: square


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