**********************
Two-dimensional Arrays
**********************

:Authors: Daniel Shiffman; Arihant Parsoya (p5 port)
:Copyright: This tutorial is from the book `Learning Processing
   <https://processing.org/books/#shiffman>`_ by Daniel Shiffman,
   published by Morgan Kaufmann, © 2008 Elsevier Inc. All rights
   reserved. The tutorial was ported to p5 by Arihant Parsoya. If you see
   any errors or have comments, open an issue on either the `p5
   <https://github.com/p5py/p5/issues>`_ or `Processing
   <https://github.com/processing/processing-docs/issues?q=is%3Aopen>`_
   repositories.

An array keeps track of multiple pieces of information in linear order, a one-dimensional list. However, the data associated with certain systems (a digital image, a board game, etc.) lives in two dimensions. To visualize this data, we need a multi-dimensional data structure, that is, a multi-dimensional array. A two-dimensional array is really nothing more than an array of arrays (a three-dimensional array is an array of arrays of arrays). Think of your dinner. You could have a one-dimensional list of everything you eat:

.. code:: python

	(lettuce, tomatoes, steak, mashed potatoes, cake, ice cream)

Or you could have a two-dimensional list of three courses, each containing two things you eat:

.. code:: python

	(lettuce, tomatoes) and (steak, mashed potatoes) and (cake, ice cream)

In the case of an array, our old-fashioned one-dimensional array looks like this:

.. code:: python
	
	myArray = [0,1,2,3]

And a two-dimensional array looks like this:

.. code:: python
	
	myArray = [[0,1,2,3], [3,2,1,0], [3,5,6,1], [3,8,3,4]]

For our purposes, it is better to think of the two-dimensional array as a matrix. A matrix can be thought of as a grid of numbers, arranged in rows and columns, kind of like a bingo board. We might write the two-dimensional array out as follows to illustrate this point: 

.. code:: python
	
	myArray = [
		[0,1,2,3], 
		[3,2,1,0], 
		[3,5,6,1], 
		[3,8,3,4]]

We can use this type of data structure to encode information about an image. For example, the following grayscale image could be represented by the following array:


.. image:: ./two-dimensional-array-res/grid.jpg
	:align: center
	:width: 50%


.. code:: python

	myArray = [
		[236, 189, 189,   0],
		[236,  80, 189, 189],
		[236,   0, 189,  80],
		[236, 189, 189,  80]]

To walk through every element of a one-dimensional array, we use a for loop, that is:

.. code:: python

	for i in range(len(myArray)):
		myArray[i] = 0

For a two-dimensional array, in order to reference every element, we must use two nested loops. This gives us a counter variable for every column and every row in the matrix.

.. code:: python

	rows = 10
	columns = 10

	for i in range(rows):
		for j in range(columns):
			myArray[i][j] = 0

For example, we might write a program using a two-dimensional array to draw a grayscale image.

.. image:: ./two-dimensional-array-res/points.jpg
	:align: center
	:width: 50%

.. code:: python

	from p5 import *

	myArray = []
	rows = None
	columns = None

	def setup():

		size(200, 200)
		global rows, columns, myArray
		columns = width
		rows = height

		for i in range(rows):
			myArray.append([])
			for j in range(columns):
				myArray[i].append(int(random_uniform(255)))

	def draw():
		global rows, columns, myArray
		for i in range(rows):
			for j in range(columns):
				stroke(myArray[i][j])
				point(i, j)

	if __name__ == '__main__':
		run()

A two-dimensional array can also be used to store objects, which is especially convenient for programming sketches that involve some sort of "grid" or "board." The following example displays a grid of Cell objects stored in a two-dimensional array. Each cell is a rectangle whose brightness oscillates from 0-255 with a sine function.

.. image:: ./two-dimensional-array-res/cells.jpg
	:align: center
	:width: 50%
	
.. code:: python

	from p5 import *

	grid = []

	# Number of columns and rows in the grid
	rows = 10
	columns = 10

	def setup():

		size(200, 200)
		global rows, columns, grid

		for i in range(rows):
			grid.append([])
			for j in range(columns):
				grid[i].append(Cell(i*20,j*20,20,20,i+j))

	def draw():
		global rows, columns, grid
		for i in range(columns):
			for j in range(rows):
				grid[i][j].oscillate()
				grid[i][j].display()

	class Cell:
		def __init__(self, tempX, tempY, tempW, tempH, tempAngle):
			self.x = tempX
			self.y = tempY
			self.w = tempW
			self.h = tempH
			self.angle = tempAngle

		def oscillate(self):
			self.angle += 0.02

		def display(self):
			stroke(255)
			# Color calculated using sine wave
			fill(127+127*sin(self.angle))
			rect((self.x, self.y), self.w, self.h)

	if __name__ == '__main__':
		run()