***********
Mouse Press
***********

.. raw:: html

  <script>
	
	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		background(230);
		strokeWeight(2);
	}

	function draw() {
		if (mouseIsPressed) {
			stroke(255);
		} else {
			stroke(237, 34, 93);
		}
		line(mouseX - 66, mouseY, mouseX + 66, mouseY);
		line(mouseX, mouseY - 66, mouseX, mouseY + 66);
	}

  </script>
  <div id="sketch-holder"></div>

Move the mouse to position the shape. Press the mouse button to invert the color.

.. code:: python

	from p5 import *

	def setup():
		size(640, 360)
		no_smooth()
		fill(126)
		background(102)

	def draw():
		if mouse_is_pressed:
			stroke(255)
		else:
			stroke(0)

		line((mouse_x-66, mouse_y), (mouse_x+66, mouse_y))
		line((mouse_x, mouse_y-66), (mouse_x, mouse_y+66)) 

	if __name__ == '__main__':
		run()