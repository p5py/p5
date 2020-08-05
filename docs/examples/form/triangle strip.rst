**************
Triangle Strip
**************

.. raw:: html

	<script>

	let x;
	let y;
	let outsideRadius = 150;
	let insideRadius = 100;

	function setup() {
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
		background(204);
		x = width / 2;
		y = height / 2;
	}

	function draw() {
		background(204);

		let numPoints = int(map(mouseX, 0, width, 6, 60));
		let angle = 0;
		let angleStep = 180.0 / numPoints;

		beginShape(TRIANGLE_STRIP);
		for (let i = 0; i <= numPoints; i++) {
			let px = x + cos(radians(angle)) * outsideRadius;
			let py = y + sin(radians(angle)) * outsideRadius;
			angle += angleStep;
			vertex(px, py);
			px = x + cos(radians(angle)) * insideRadius;
			py = y + sin(radians(angle)) * insideRadius;
			vertex(px, py);
			angle += angleStep;
		}
		endShape();
	}

	</script>
	<div id="sketch-holder"></div>

Example by Ira Greenberg. Generate a closed ring using the vertex() function and beginShape(TRIANGLE_STRIP) mode. The outsideRadius and insideRadius variables control ring's radii respectively.

.. code:: python

	from p5 import *

	x = 0
	y = 0
	outsideRadius = 150
	insideRadius = 100

	def setup():
		size(720, 400)
		background(204)

		global x, y
		x = width / 2
		y = height / 2

	def draw():
		global x, y, outsideRadius, insideRadius
		background(204)

		numPoints = int(remap(mouse_x, [0, width], [6, 60]))
		angle = 0
		angleStep = 180.0 / numPoints

		begin_shape(TRIANGLE_STRIP)

		for i in range(numPoints + 1):
			px = x + cos(radians(angle)) * outsideRadius
			py = y + sin(radians(angle)) * outsideRadius
			angle += angleStep
			vertex(px, py)

			px = x + cos(radians(angle)) * insideRadius
			py = y + sin(radians(angle)) * insideRadius
			vertex(px, py)

			angle += angleStep

		end_shape()

	if __name__ == '__main__':
		run()