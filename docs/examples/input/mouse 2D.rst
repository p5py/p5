********
Mouse 2D
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
		fill(244, 122, 158);
		rect(mouseX, height / 2, mouseY / 2 + 10, mouseY / 2 + 10);
		fill(237, 34, 93);
		let inverseX = width - mouseX;
		let inverseY = height - mouseY;
		rect(inverseX, height / 2, inverseY / 2 + 10, inverseY / 2 + 10);
	}
  </script>
  <div id="sketch-holder"></div>

Moving the mouse changes the position and size of each box.

.. code:: python

	from p5 import *

	def setup():
		size(640, 360)
		no_stroke()
		rect_mode("CENTER")

	def draw():
		background(230)

		background(51)
		fill(255, 204)
		rect((mouse_x, height/2), mouse_y/2+10, mouse_y/2+10)
		
		fill(255, 204)
		inverseX = width - mouse_x
		inverseY = height - mouse_y
		rect((inverseX, height/2), (inverseY/2)+10, (inverseY/2)+10);

	if __name__ == '__main__':
		run()