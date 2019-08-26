*********
Translate
*********

.. raw:: html

  <script>
	let x = 0;
	let y = 0;
	let dim = 80.0;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  noStroke();
	}

	function draw() {
	  background(102);
	  // Animate by increasing our x value
	  x = x + 0.8;
	  // If the shape goes off the canvas, reset the position
	  if (x > width + dim) {
	    x = -dim;
	  }

	  // Even though our rect command draws the shape with its
	  // center at the origin, translate moves it to the new
	  // x and y position
	  translate(x, height / 2 - dim / 2);
	  fill(255);
	  rect(-dim / 2, -dim / 2, dim, dim);

	  // Transforms accumulate. Notice how this rect moves
	  // twice as fast as the other, but it has the same
	  // parameter for the x-axis value
	  translate(x, dim);
	  fill(0);
	  rect(-dim / 2, -dim / 2, dim, dim);
	}
  </script>
  <div id="sketch-holder"></div>

The ``translate()`` function allows objects to be moved to any location within the window. The first parameter sets the x-axis offset and the second parameter sets the y-axis offset.

.. code:: python

	from p5 import *

	x = 0
	y = 0
	dim = 80.0

	def setup():
		size(640, 360) 	
		no_stroke()	  

	def draw():
		background(102)

		global x
		x = x + 0.8

		if x > width + dim:
			x = -dim

		translate(x, height/2 - dim/2)
		fill(255)
		rect((-dim/2, -dim/2), dim, dim)

		# Transforms accumulate. Notice how this rect moves 
	  	# twice as fast as the other, but it has the same 
	  	# parameter for the x-axis value
		translate(x, dim)
		fill(0)
		rect((-dim/2, -dim/2), dim, dim)

	if __name__ == '__main__':
	  run()
