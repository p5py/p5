**********
Relativity
**********

.. raw:: html

  <script>
  	let a, b, c, d, e;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  noStroke();
	  a = color(165, 167, 20);
	  b = color(77, 86, 59);
	  c = color(42, 106, 105);
	  d = color(165, 89, 20);
	  e = color(146, 150, 127);
	  noLoop(); // Draw only one time
	}

	function draw() {
	  drawBand(a, b, c, d, e, 0, width / 128);
	  drawBand(c, a, d, b, e, height / 2, width / 128);
	}

	function drawBand(v, w, x, y, z, ypos, barWidth) {
	  let num = 5;
	  let colorOrder = [v, w, x, y, z];
	  for (let i = 0; i < width; i += barWidth * num) {
	    for (let j = 0; j < num; j++) {
	      fill(colorOrder[j]);
	      rect(i + j * barWidth, ypos, barWidth, height / 2);
	    }
	  }
	}
  </script>
  <div id="sketch-holder"></div>

Each color is perceived in relation to other colors. The top and bottom bars each contain the same component colors, but a different display order causes individual colors to appear differently.

.. code:: python

	from p5 import *

	a = b = c = d = e = None

	def setup():
		size(640, 360)
		no_stroke()

		global a, b, c, d, e
		a = Color(165, 167, 20)
		b = Color(77, 86, 59)
		c = Color(42, 106, 105)
		d = Color(165, 89, 20)
		e = Color(146, 150, 127)

		no_loop()


	def draw():
		global a, b, c, d, e
		drawBand(a, b, c, d, e, 0, width/128)
		drawBand(c, a, d, b, e, height/2, width/128)

	def drawBand(v, w, x, y, z, ypos, barWidth):
		num = 5
		colorOrder = [v, w, x, y, z]

		for i in range(0, width, int(barWidth*num)):
			for j in range(num):
				fill(colorOrder[j])
				rect((i + j*barWidth, ypos), barWidth, height/2)

	if __name__ == '__main__':
	  run()
