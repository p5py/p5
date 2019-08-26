***************
Linear Gradient
***************

.. raw:: html

  <script>
	// Constants
	const Y_AXIS = 1;
	const X_AXIS = 2;
	let b1, b2, c1, c2;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');

	  // Define colors
	  b1 = color(255);
	  b2 = color(0);
	  c1 = color(204, 102, 0);
	  c2 = color(0, 102, 153);

	  noLoop();
	}

	function draw() {
	  // Background
	  setGradient(0, 0, width / 2, height, b1, b2, X_AXIS);
	  setGradient(width / 2, 0, width / 2, height, b2, b1, X_AXIS);
	  // Foreground
	  setGradient(50, 90, 540, 80, c1, c2, Y_AXIS);
	  setGradient(50, 190, 540, 80, c2, c1, X_AXIS);
	}

	function setGradient(x, y, w, h, c1, c2, axis) {
	  noFill();

	  if (axis === Y_AXIS) {
	    // Top to bottom gradient
	    for (let i = y; i <= y + h; i++) {
	      let inter = map(i, y, y + h, 0, 1);
	      let c = lerpColor(c1, c2, inter);
	      stroke(c);
	      line(x, i, x + w, i);
	    }
	  } else if (axis === X_AXIS) {
	    // Left to right gradient
	    for (let i = x; i <= x + w; i++) {
	      let inter = map(i, x, x + w, 0, 1);
	      let c = lerpColor(c1, c2, inter);
	      stroke(c);
	      line(i, y, i, y + h);
	    }
	  }
	}

  </script>
  <div id="sketch-holder"></div>

The ``lerpColor()`` function is useful for interpolating between two colors.

.. code:: python

	from p5 import *

	Y_AXIS = 1
	X_AXIS = 2
	b1 = b2 = c1 = c2 = None

	def setup():
		size(640, 360)

		global b1, b2, c1, c2
		b1 = Color(255)
		b2 = Color(0)
		c1 = Color(204, 102, 0)
		c2 = Color(0, 102, 153)

		no_loop()


	def draw():
		global b1, b2, c1, c2

		# background
		setGradient(0, 0, width/2, height, b1, b2, X_AXIS)
		setGradient(width/2, 0, width/2, height, b2, b1, X_AXIS)
	  	# Foreground
		setGradient(50, 90, 540, 80, c1, c2, Y_AXIS)
		setGradient(50, 190, 540, 80, c2, c1, X_AXIS)

	def setGradient(x, y, w, h, c1, c2, axis):
		no_fill()

		if axis == Y_AXIS:
			for i in range(y, y + int(h) + 1):
				inter = remap(i, [y, y+h], [0, 1])
				c = c1.lerp(c2, inter)
				stroke(c)
				line((x, i), (x+w, i))
		elif axis == X_AXIS:
			for i in range(int(x), int(x + w) + 1):
				inter = remap(i, [x, x+w], [0, 1])
				c = c1.lerp(c2, inter)
				stroke(c)
				line((i, y), (i, y+h))

	if __name__ == '__main__':
	  run()

