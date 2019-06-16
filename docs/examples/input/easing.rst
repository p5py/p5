******
Easing
******

.. raw:: html

	<script>
	let x = 1;
	let y = 1;
	let easing = 0.05;

	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		noStroke();
	}

	function draw() {
		background(237, 34, 93);
		let targetX = mouseX;
		let dx = targetX - x;
		x += dx * easing;

		let targetY = mouseY;
		let dy = targetY - y;
		y += dy * easing;

		ellipse(x, y, 66, 66);
	}
	</script>
	<div id="sketch-holder"></div>

Move the mouse across the screen and the symbol will follow. Between drawing each frame of the animation, the program calculates the difference between the position of the symbol and the cursor. If the distance is larger than 1 pixel, the symbol moves part of the distance (0.05) from its current position toward the cursor.

.. code:: python

	from p5 import *

	x = 0
	y = 0
	easing = 0.05

	def setup():
		size(640, 360)
		no_stroke()

	def draw():
		background(51)

		global x, y, easing
		targetX = mouse_x
		dx = targetX - x
		x += dx * easing

		targetY = mouse_y
		dy = targetY - y
		y += dy * easing

		ellipse((x, y), 66, 66)

	if __name__ == '__main__':
		run()
