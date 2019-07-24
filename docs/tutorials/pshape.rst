******
PShape
******

:Authors: Daniel Shiffman; Arihant Parsoya (p5 port)

:Copyright: This tutorial is "Extension 5" from `Processing: A
   Programming Handbook for Visual Designers and Artists, Second
   Edition <https://processing.org/handbook>`_, published by MIT
   Press. © 2014 MIT Press. If you see any errors or have comments,
   please let us know. The tutorial was ported to p5 by Arihant Parsoya. If
   you see any errors or have comments, open an issue on either the
   `p5 <https://github.com/p5py/p5/issues>`_ or `Processing
   <https://github.com/processing/processing-docs/issues?q=is%3Aopen>`_
   repositories.

One of the very first things you learn when programming with Processing is how to draw "primitive" shapes to the screen: rectangles, ellipses, lines, triangles, and more.

.. code:: python

	rect((x,y),w,h)
	ellipse((x,y),w,h)
	line((x1,y1),(x2,y2))
	triangle((x1,y1),(x2,y2),(x3,y3))

A more advanced drawing option is to use ``beginShape()`` and ``endShape()`` to specify the vertices of a custom polygon

.. code:: python

	beginShape()
	vertex(x1,y1)
	vertex(x2,y2)
	vertex(x3,y3)
	vertex(x4,y4)
	# etc
	endShape()

And you can build more complex shapes by grouping a set of drawing functions together, even perhaps organizing them into a class.

.. code:: python

	class MyWackyShape:

		# constructor 

		# some functions

		def display():
			beginShape()
			vertex(x1,y1)
			vertex(x2,y2)
			vertex(x3,y3)
			vertex(x4,y4)
			# etc
			endShape()

This is all well and good and will get you pretty far. There's very little you can't draw just knowing the above. However, there is another step. A step that can, in some cases, improve the speed of your rendering as well as offer a more advanced organizational model for your code—PShape.

PShape is a datatype for storing shapes. These can be shapes that you build out of custom geometry or shapes that you load from an external file, such as an SVG.

Primitive PShapes
=================

Let's begin with one of the simplest cases for use of a PShape. Here's a simple Processing ``draw()`` method that draws an rectangle following the mouse.

.. image:: ./pshape-res/pshape1.png
   :align: center


.. code:: python

	def draw():
		background(51)
		stroke(255)
		fill(127)
		rect((mouse_x, mouse_y), 100, 50)

Pretty basic stuff. If this was all the code we had, there's not necessarily a good reason for using a PShape instead, but we're going to push ahead and make a PShape rectangle anyway as a demonstration. Our goal here is to have a variable that stores the color and dimensions of that variable, allowing our draw function to look like this.

.. code:: python

	def draw():
		background(51)
		shape(rectangle)

And what is this "rectangle"? It's a PShape.

