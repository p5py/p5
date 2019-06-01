*****
Array
*****

.. raw:: html

  <script>
	let coswave = [];

	function setup() {
		var canvas = createCanvas(720, 360);
  	  	canvas.parent('sketch-holder');
		for (let i = 0; i < width; i++) {
			let amount = map(i, 0, width, 0, PI);
			coswave[i] = abs(cos(amount));
		}
		background(255);
		noLoop();
	}

	function draw() {
		  let y1 = 0;
		  let y2 = height / 3;
		  for (let i = 0; i < width; i += 3) {
			    stroke(coswave[i] * 255);
			    line(i, y1, i, y2);
		  }

		  y1 = y2;
		  y2 = y1 + y1;
		  for (let i = 0; i < width; i += 3) {
			    stroke((coswave[i] * 255) / 4);
			    line(i, y1, i, y2);
		  }

		  y1 = y2;
		  y2 = height;
		  for (let i = 0; i < width; i += 3) {
			    stroke(255 - coswave[i] * 255);
			    line(i, y1, i, y2);
		  }
	}
  </script>
  <div id="sketch-holder"></div>

An array is a list of data. Each piece of data in an array is identified by an index number representing its position in the array. Arrays are zero based, which means that the first element in the array is [0], the second element is [1], and so on. In this example, an array named "coswave" is created and filled with the cosine values. This data is displayed three separate ways on the screen.

.. code:: python

	from p5 import *

	coswave = []

	def setup():
		size(720, 360)
		for i in range(width):
			amount = remap(i, [0, width], [0, PI])
			coswave.append(abs(cos(amount)))
		
		background(255)
		no_loop()

	def draw():
		y1 = 0
		y2 = height/3
		for i in range(0, width, 3):
			stroke(coswave[i] * 255)
			line((i, y1), (i, y2))

		y1 = y2
		y2 = y1 + y1
		for i in range(0, width, 3):
			stroke(coswave[i]*255 / 4)
			line((i, y1), (i, y2))

		y1 = y2
		y2 = height
		for i in range(0, width, 3):
			stroke(255 - coswave[i] * 255)
			line((i, y1), (i, y2))

	if __name__ == '__main__':
	  run()
