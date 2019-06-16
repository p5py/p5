********
Mouse 1D
********

.. raw:: html

	<script>
	let bx;
	let by;
	let boxSize = 75;
	let overBox = false;
	let locked = false;
	let xOffset = 0.0;
	let yOffset = 0.0;

	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		bx = width / 2.0;
		by = height / 2.0;
		rectMode(RADIUS);
		strokeWeight(2);
	}

	function draw() {
		background(237, 34, 93);

		// Test if the cursor is over the box
		if (
			mouseX > bx - boxSize &&
			mouseX < bx + boxSize &&
			mouseY > by - boxSize &&
			mouseY < by + boxSize
		) {
			overBox = true;
			if (!locked) {
				stroke(255);
				fill(244, 122, 158);
			}
		} else {
			stroke(156, 39, 176);
			fill(244, 122, 158);
			overBox = false;
		}

		// Draw the box
		rect(bx, by, boxSize, boxSize);
	}

	function mousePressed() {
		if (overBox) {
			locked = true;
			fill(255, 255, 255);
		} else {
			locked = false;
		}
		xOffset = mouseX - bx;
		yOffset = mouseY - by;
	}

	function mouseDragged() {
		if (locked) {
			bx = mouseX - xOffset;
			by = mouseY - yOffset;
		}
	}

	function mouseReleased() {
		locked = false;
	}

	</script>
	<div id="sketch-holder"></div>

Click on the box and drag it across the screen.

.. code:: python

	from p5 import *

	bx = 0
	by = 0
	boxSize = 75
	overBox = False
	locked = False
	xOffset = 0.0
	yOffset = 0.0

	def setup():
		size(640, 360)

		global bx, by
		bx = width/2.0
		by = height/2.0
		rect_mode("RADIUS")

	def draw():
		background(0)

		global bx, by, boxSize, overBox, locked, xOffset, yOffset

		# Test if the cursor is over the box
		if (mouse_x > bx-boxSize and mouse_x < bx+boxSize and 
		    	mouse_y > by-boxSize and mouse_y < by+boxSize):
			overBox = True

			if not locked:
				stroke(255)
				fill(153)

		else:
			stroke(153)
			fill(153)
			overBox = False

		rect([bx, by], boxSize, boxSize)

	def mouse_pressed():
		global bx, by, boxSize, overBox, locked, xOffset, yOffset

		if overBox:
			locked = True
			fill(255, 255, 255)
		else:
			locked = False

		xOffset = mouse_x - bx
		yOffset = mouse_y - by

	def mouse_dragged():
		global bx, by, boxSize, overBox, locked, xOffset, yOffset
		if locked:
			bx = mouse_x - xOffset
			by = mouse_y - yOffset

	def mouse_released():
		global locked
		locked = False


	if __name__ == '__main__':
		run()