****************
Shape Primitives
****************

.. raw:: html

	<script>
	function setup() {
		// Sets the screen to be 720 pixels wide and 400 pixels high
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
		background(0);
		noStroke();

		fill(204);
		triangle(18, 18, 18, 360, 81, 360);

		fill(102);
		rect(81, 81, 63, 63);

		fill(204);
		quad(189, 18, 216, 18, 216, 360, 144, 360);

		fill(255);
		ellipse(252, 144, 72, 72);

		fill(204);
		triangle(288, 18, 351, 360, 288, 360);

		fill(255);
		arc(479, 300, 280, 280, PI, TWO_PI);
	}
	</script>
	<div id="sketch-holder"></div>

The basic shape primitive functions are ``triangle()``, ``rect()``, ``quad()``, ``ellipse()``, and ``arc()``. Squares are made with ``rect()`` and circles are made with ``ellipse()``. Each of these functions requires a number of parameters to determine the shape's position and size.

.. code:: python

	from p5 import *

	def setup():
		# Sets the screen to be 720 pixels wide and 400 pixels high
		size(720, 400)
		no_loop()

	def draw():
		background(0)
		no_stroke()

		fill(204)
		triangle((18, 18), (18, 360), (81, 360))

		fill(102)
		rect((81, 81), 63, 63)

		fill(204)
		quad((189, 18), (216, 18), (216, 360), (144, 360))

		fill(255)
		ellipse((252, 144), 72, 72)

		fill(204)
		triangle((288, 18), (351, 360), (288, 360))

		fill(255)
		arc((479, 300), 280, 280, PI, TWO_PI)

	if __name__ == '__main__':
		run()