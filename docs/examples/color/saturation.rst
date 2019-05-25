**********
Saturation
**********

.. raw:: html

  <script>
	const barWidth = 20;
	let lastBar = -1;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  colorMode(HSB, width, height, 100);
	  noStroke();
	}

	function draw() {
	  let whichBar = mouseX / barWidth;
	  if (whichBar !== lastBar) {
	    let barX = whichBar * barWidth;
	    fill(barX, mouseY, 66);
	    rect(barX, 0, barWidth, height);
	    lastBar = whichBar;
	  }
	}
  </script>
  <div id="sketch-holder"></div>

Saturation is the strength or purity of the color and represents the amount of gray in proportion to the hue. A "saturated" color is pure and an "unsaturated" color has a large percentage of gray. Move the cursor vertically over each bar to alter its saturation.

.. code:: python

	from p5 import *

	barWidth = 20
	lastBar = -1

	def setup():
		size(640, 360)
		color_mode('HSB', height, height, height)	  
		no_stroke()

	def draw():
		global barWidth, lastBar

		whichBar = mouse_x / barWidth
		if whichBar != lastBar:
			barX = whichBar*barWidth
			fill(barX, mouse_y, height)
			rect((barX, 0), barWidth, height)
			lastBar = whichBar

	if __name__ == '__main__':
	  run()
