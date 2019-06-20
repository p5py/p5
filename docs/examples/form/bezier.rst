******
Bezier
******

.. raw:: html

	<script>
	function setup() {
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
		stroke(255);
		noFill();
	}

	function draw() {
		background(0);
		for (let i = 0; i < 200; i += 20) {
			bezier(
				mouseX - i / 2.0,
				40 + i,
				410,
				20,
				440,
				300,
				240 - i / 16.0,
				300 + i / 8.0
			);
		}
	}
	</script>
	<div id="sketch-holder"></div>

The first two parameters for the ``bezier()`` function specify the first point in the curve and the last two parameters specify the last point. The middle parameters set the control points that define the shape of the curve.


.. code:: python

	from p5 import *

	def setup():
		size(720, 400)
		stroke(255)
		no_fill()

	def draw():
		background(0)

		for i in range(0, 200, 20):
			bezier(
				(mouse_x - i / 2.0, 40 + i),
				(410, 20),
				(440, 300),
				(240 - i / 16.0, 300 + i / 8.0)
				)

	if __name__ == '__main__':
		run()