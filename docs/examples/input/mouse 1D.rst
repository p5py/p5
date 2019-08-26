********
Mouse 1D
********

.. raw:: html

	<script>
	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		noStroke();
		rectMode(CENTER);
	}

	function draw() {
		background(230);

		let r1 = map(mouseX, 0, width, 0, height);
		let r2 = height - r1;

		fill(237, 34, 93, r1);
		rect(width / 2 + r1 / 2, height / 2, r1, r1);

		fill(237, 34, 93, r2);
		rect(width / 2 - r2 / 2, height / 2, r2, r2);
	}
	</script>
	<div id="sketch-holder"></div>

Move the mouse left and right to shift the balance. The "mouse_x" variable is used to control both the size and color of the rectangles.

.. code:: python

	from p5 import *

	def setup():
		size(720, 400)
		no_stroke()
		rect_mode("CENTER")

	def draw():
		background(230)

		r1 = remap(mouse_x, [0, width], [0, height])
		r2 = height - r1

		fill(237, 34, 93, r1)
		rect([width / 2 + r1 / 2, height / 2], r1, r1)

		fill(237, 34, 93, r2)
		rect([width / 2 - r2 / 2, height / 2], r2, r2)

	if __name__ == '__main__':
		run()