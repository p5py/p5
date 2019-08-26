**********
Brightness
**********

.. raw:: html

  <script>
	let img;

	function preload() {
	  img = loadImage('assets/moonwalk.jpg');
	}

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  pixelDensity(1);
	  img.loadPixels();
	  loadPixels();
	}

	function draw() {
	  for (let x = 0; x < img.width; x++) {
	    for (let y = 0; y < img.height; y++) {
	      // Calculate the 1D location from a 2D grid
	      let loc = (x + y * img.width) * 4;
	      // Get the R,G,B values from image
	      let r, g, b;
	      r = img.pixels[loc];
	      // Calculate an amount to change brightness based on proximity to the mouse
	      let maxdist = 50;
	      let d = dist(x, y, mouseX, mouseY);
	      let adjustbrightness = (255 * (maxdist - d)) / maxdist;
	      r += adjustbrightness;
	      // Constrain RGB to make sure they are within 0-255 color range
	      r = constrain(r, 0, 255);
	      // Make a new color and set pixel in the window
	      //color c = color(r, g, b);
	      let pixloc = (y * width + x) * 4;
	      pixels[pixloc] = r;
	      pixels[pixloc + 1] = r;
	      pixels[pixloc + 2] = r;
	      pixels[pixloc + 3] = 255;
	    }
	  }
	  updatePixels();
	}

  </script>
  <div id="sketch-holder"></div>

This program adjusts the brightness of a part of the image by calculating the distance of each pixel to the mouse.

.. code:: python

	from p5 import *

	bar_width = 20
	last_bar = None

	def setup():
	    size(640, 360)
	    title("Brightness")
	    color_mode('HSB', width, 100, height)
	    no_stroke()
	    background(0)

	def draw():
	    global last_bar
	    which_bar = mouse_x // bar_width
	    if which_bar is not last_bar:
	        bar_x = which_bar * bar_width
	        fill(bar_x, 100, mouse_y)
	        rect((bar_x, 0), bar_width, height)
	        last_bar = which_bar

	if __name__ == '__main__':
	    run()