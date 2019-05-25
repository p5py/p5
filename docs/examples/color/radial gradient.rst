***************
Radial Gradient
***************

.. raw:: html

  <script>
	let dim;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  dim = width / 2;
	  background(0);
	  colorMode(HSB, 360, 100, 100);
	  noStroke();
	  ellipseMode(RADIUS);
	  frameRate(1);
	}

	function draw() {
	  background(0);
	  for (let x = 0; x <= width; x += dim) {
	    drawGradient(x, height / 2);
	  }
	}

	function drawGradient(x, y) {
	  let radius = dim / 2;
	  let h = random(0, 360);
	  for (let r = radius; r > 0; --r) {
	    fill(h, 90, 90);
	    ellipse(x, y, r, r);
	    h = (h + 1) % 360;
	  }
	}

  </script>
  <div id="sketch-holder"></div>

Draws a series of concentric circles to create a gradient from one color to another.

.. code:: python

	from p5 import *

	dim = None

	def setup():
		size(640, 360)

		global dim
		dim = width/2;
		background(0)
		color_mode('HSB', 360, 100, 100)
		no_stroke()

	def draw():
		global dim
		background(0)

		x = 0
		while x <= width:
			drawGradient(x, height/2)
			x += dim		

	def drawGradient(x, y):
		radius = dim/2
		h = random_uniform(0, 360)

		for r in range(int(radius), 0, -1):
			fill(h, 90, 90)
			ellipse((x, y), r*2, r*2)
			h = (h + 1) % 360

	if __name__ == '__main__':
	  run(frame_rate=1)
