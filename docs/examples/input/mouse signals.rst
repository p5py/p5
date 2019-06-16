*************
Mouse Signals
*************

.. raw:: html

	<script>
	let xvals = [];
	let yvals = [];
	let bvals = [];

	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		strokeWeight(2);
	}

	function draw() {
		background(237, 34, 93);

		for (let i = 1; i < width; i++) {
			xvals[i - 1] = xvals[i];
			yvals[i - 1] = yvals[i];
			bvals[i - 1] = bvals[i];
		}
		// Add the new values to the end of the array
		xvals[width - 1] = mouseX;
		yvals[width - 1] = mouseY;

		if (mouseIsPressed) {
			bvals[width - 1] = 0;
		} else {
			bvals[width - 1] = 255;
		}

		fill(255);
		noStroke();
		rect(0, height / 3, width, height / 3 + 1);

		for (let i = 1; i < width; i++) {
			stroke(255);
			point(i, xvals[i] / 3);
			stroke(0);
			point(i, height / 3 + yvals[i] / 3);
			stroke(255);
			line(
				i,
				(2 * height) / 3 + bvals[i] / 3,
				i,
				(2 * height) / 3 + bvals[i - 1] / 3
			);
		}
	}

	</script>
	<div id="sketch-holder"></div>

Move and click the mouse to generate signals. The top row is the signal from "mouse_x", the middle row is the signal from "mouse_y", and the bottom row is the signal from "mouse_is_pressed".

.. code:: python

	from p5 import *

	xvals = None
	yvals = None
	bvals = None
	arrayindex = 0

	def setup():
		size(640, 360)
		no_smooth()

		global xvals, yvals, bvals
		xvals = [0]*width
		yvals = [0]*width
		bvals = [0]*width

	def draw():
		background(102);

		global xvals, yvals, bvals
		for i in range(1, width):
			xvals[i-1] = xvals[i] 
			yvals[i-1] = yvals[i]
			bvals[i-1] = bvals[i]

		xvals[width - 1] = mouse_x
		yvals[width - 1] = mouse_y

		if mouse_is_pressed: 
			bvals[width-1] = 0;
		else:
			bvals[width-1] = 255;
		

		fill(255)
		no_stroke()
		rect((0, height/3), width, height/3+1)

		for i in range(1, width):
			stroke(255)
			point(i, remap(xvals[i], [0, width], [0, height/3 - 1]))
			stroke(0)
			point(i, height/3 + yvals[i]/3)
			stroke(255)
			line([i, 2*height/3 + bvals[i]/3], [i, (2*height/3 + bvals[i - 1]/3)])

	if __name__ == '__main__':
		run()