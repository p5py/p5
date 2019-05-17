**************
Setup and Draw
**************

.. raw:: html

  <script>
	let y = 100;
    function setup() {
      	var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		stroke(255); // Set line drawing color to white
  		frameRate(30);
    }

    function draw() {
			background(0); // Set the background to black
			y = y - 1;
			if (y < 0) {
				y = height;
			}
			line(0, y, width, y);
    }
    </script>
    <div id="sketch-holder"></div>

The code inside the draw() function runs continuously from top to bottom until the program is stopped.

.. code:: python

	from p5 import *

	# The statement in setup() function
	# ececute once when the program begins
	def setup():
		size(640, 360) # size must be the first statement
		stroke(255) # Set line drawing color to white
		y = 0

	# The statements in draw() are executed until the
	# program is stopped. Each statement is executed in
	# sequence and after the last line is read, the first
	# line is executed again.
	def draw():
		background(0) # Clear the screen with a black background
		y = y - 1
		if y < 0:
			y = height

		line((0, y), (width, y))


	if __name__ == '__main__':
	    run()
