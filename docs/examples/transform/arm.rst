***
Arm
***

.. raw:: html

  <script>
	let x, y;
	let angle1 = 0.0;
	let angle2 = 0.0;
	let segLength = 100;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  strokeWeight(30);

	  //Stroke with a semi-transparent white
	  stroke(255, 160);

	  //Position the "shoulder" of the arm in the center of the canvas
	  x = width * 0.5;
	  y = height * 0.5;
	}

	function draw() {
	  background(0);

	  //Change the angle of the segments according to the mouse positions
	  angle1 = (mouseX / float(width) - 0.5) * -TWO_PI;
	  angle2 = (mouseY / float(height) - 0.5) * PI;

	  //use push and pop to "contain" the transforms. Note that
	  // even though we draw the segments using a custom function,
	  // the transforms still accumulate
	  push();
	  segment(x, y, angle1);
	  segment(segLength, 0, angle2);
	  pop();
	}

	//a custom function for drawing segments
	function segment(x, y, a) {
	  translate(x, y);
	  rotate(a);
	  line(0, 0, segLength, 0);
	}
  </script>
  <div id="sketch-holder"></div>

The angle of each segment is controlled with the mouseX and mouseY position. The transformations applied to the first segment are also applied to the second segment because they are inside the same ``pushMatrix()`` and ``popMatrix()`` group.

.. code:: python

	from p5 import *

	x = 0
	y = 0
	angle1 = 0.0
	angle2 = 0.0
	segLength = 100

	def setup():
		size(640, 360)
		stroke(255, 160)
		stroke_weight(30)

		global x, y
		x = width * 0.3
		y = height * 0.5

	def draw():
		background(0)

		angle1 = (mouse_x/width - 0.5) * -PI
		angle2 = (mouse_y/height - 0.5) * PI

		with push_matrix():
			segment(x, y, angle1)
			segment(segLength, 0, angle2)

	def segment(x, y, a):
		translate(x, y)
		rotate(a)
		line((0, 0), (segLength, 0))

	if __name__ == '__main__':
	  run()
