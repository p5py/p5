********
Array 2D
********

.. raw:: html

  <script>
	let distances = [];
	let maxDistance;
	let spacer;

	function setup() {
	  	var canvas = createCanvas(720, 360);
  	  	canvas.parent('sketch-holder');
	  	maxDistance = dist(width / 2, height / 2, width, height);
	  	for (let x = 0; x < width; x++) {
		    distances[x] = []; // create nested array
		    for (let y = 0; y < height; y++) {
		      	let distance = dist(width / 2, height / 2, x, y);
		      	distances[x][y] = (distance / maxDistance) * 255;
		    }
		}
	  	spacer = 10;
	  	noLoop(); // Run once and stop
	}

	function draw() {
		background(0);
		// This embedded loop skips over values in the arrays based on
		// the spacer variable, so there are more values in the array
		// than are drawn here. Change the value of the spacer variable
		// to change the density of the points
		for (let x = 0; x < width; x += spacer) {
			for (let y = 0; y < height; y += spacer) {
				stroke(distances[x][y]);
				point(x + spacer / 2, y + spacer / 2);
			}
		}
	}

  </script>
  <div id="sketch-holder"></div>

Demonstrates the syntax for creating a two-dimensional (2D) array. Values in a 2D array are accessed through two index values. 2D arrays are useful for storing images. In this example, each dot is colored in relation to its distance from the center of the image.

.. code:: python

	from p5 import *

	distances = []
	maxDiantance = None
	spacer = None

	def setup():
		size(720, 360)

		global distances, maxDiantance, spacer
		maxDistance = dist((width / 2, height / 2), (width, height))
		for x in range(width):
			d = []
			for y in range(height):
				distance = dist((width / 2, height / 2), (x, y))
				d.append((distance / maxDistance) * 255)
			distances.append(d)

		spacer = 10
		no_loop()

	def draw():
		background(0)

		for x in range(0, width, spacer):
			for y in range(0, height, spacer):
				stroke(distances[x][y])
				point(x + spacer / 2, y + spacer / 2)

	if __name__ == '__main__':
	  run()