***********
Mouse Input
***********

.. raw:: html

	<script>
	let num = 60;
	let mx = [];
	let my = [];

	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		noStroke();
		fill(255, 153);
		for (let i = 0; i < num; i++) {
			mx.push(i);
			my.push(i);
		}
	}

	function draw() {
		background(237, 34, 93);

		// Cycle through the array, using a different entry on each frame.
		// Using modulo (%) like this is faster than moving all the values over.
		let which = frameCount % num;
		mx[which] = mouseX;
		my[which] = mouseY;

		for (let i = 0; i < num; i++) {
			// which+1 is the smallest (the oldest in the array)
			let index = (which + 1 + i) % num;
			ellipse(mx[index], my[index], i, i);
		}
	}

	</script>
	<div id="sketch-holder"></div>

Move the mouse across the screen to change the position of the circles. The positions of the mouse are recorded into an array and played back every frame. Between each frame, the newest value are added to the end of each array and the oldest value is deleted.

.. code:: python

	from p5 import *

	num = 60
	mx = [0]*num
	my = [0]*num

	def setup():
		size(640, 360)
		no_stroke()
		fill(255, 153)

	def draw():
		background(51)

		global num, mx, my

		which = frame_count % num

		mx[which] = mouse_x
		my[which] = mouse_y

		for i in range(num):
			index = (which+1 + i) % num
			ellipse([mx[index], my[index]], i, i)

	if __name__ == '__main__':
		run()
