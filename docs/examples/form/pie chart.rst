*********
Pie Chart
*********

.. raw:: html

	<script>
	let angles = [30, 10, 45, 35, 60, 38, 75, 67];

	function setup() {
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
		noStroke();
		noLoop(); // Run once and stop
	}

	function draw() {
		background(100);
		pieChart(300, angles);
	}

	function pieChart(diameter, data) {
		let lastAngle = 0;
		for (let i = 0; i < data.length; i++) {
			let gray = map(i, 0, data.length, 0, 255);
			fill(gray);
			arc(
				width / 2,
				height / 2,
				diameter,
				diameter,
				lastAngle,
				lastAngle + radians(angles[i])
			);
			lastAngle += radians(angles[i]);
		}
	}

	</script>
	<div id="sketch-holder"></div>

Uses the ``arc()`` function to generate a pie chart from the data stored in an array.

.. code:: python

	from p5 import *

	angles = [30, 10, 45, 35, 60, 38, 75, 67]

	def setup():
		# Sets the screen to be 720 pixels wide and 400 pixels high
		size(720, 400)
		no_loop()
		no_stroke()

	def draw():
		background(100)
		pie_chart(300, angles)

	def pie_chart(diameter, data):
		lastAngle = 0
		for i in range(len(data)):
			gray = remap(i, [0, len(data)], [0, 255])
			fill(gray)
			arc(
				(width / 2, height / 2),
				diameter,
				diameter,
				lastAngle,
				lastAngle + radians(angles[i])
			)

			lastAngle += radians(angles[i])

	if __name__ == '__main__':
		run()