***
Hue
***

.. raw:: html

  <script>
	const barWidth = 20;
	let lastBar = -1;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  colorMode(HSB, height, height, height);
	  noStroke();
	  background(0);
	}

	function draw() {
	  let whichBar = mouseX / barWidth;
	  if (whichBar !== lastBar) {
	    let barX = whichBar * barWidth;
	    fill(mouseY, height, height);
	    rect(barX, 0, barWidth, height);
	    lastBar = whichBar;
	  }
	}
  </script>
  <div id="sketch-holder"></div>

Hue is the color reflected from or transmitted through an object and is typically referred to as the name of the color (red, blue, yellow, etc.) Move the cursor vertically over each bar to alter its hue.

.. code:: python

	from p5 import *

	barWidth = 20
	lastBar = -1

	def setup():
		size(640, 360)
		stroke(255, 160)
		color_mode('HSB', height, height, height)	  
		no_stroke()
		background(0)

	def draw():
		global barWidth, lastBar

		whichBar = mouse_x / barWidth
		if whichBar != lastBar:
			barX = whichBar*barWidth
			fill(mouse_x, height, height)
			rect((barX, 0), barWidth, height)
			lastBar = whichBar

	if __name__ == '__main__':
	  run()
