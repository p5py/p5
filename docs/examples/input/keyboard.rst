********
Keyboard
********

.. raw:: html

	<script>
	let rectWidth;

	function setup() {
		var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		noStroke();
		background(230);
		rectWidth = width / 4;
	}

	function draw() {
		// keep draw() here to continue looping while waiting for keys
	}

	function keyPressed() {
		let keyIndex = -1;
		if (key >= 'a' && key <= 'z') {
			keyIndex = key.charCodeAt(0) - 'a'.charCodeAt(0);
		}
		if (keyIndex === -1) {
			// If it's not a letter key, clear the screen
			background(230);
		} else {
			// It's a letter key, fill a rectangle
			randFill_r = Math.floor(Math.random() * 255 + 1);
			randFill_g = Math.floor(Math.random() * 255 + 1);
			randFill_b = Math.floor(Math.random() * 255 + 1);
			fill(randFill_r, randFill_g, randFill_b);
			let x = map(keyIndex, 0, 25, 0, width - rectWidth);
			rect(x, 0, rectWidth, height);
		}
	}

	</script>
	<div id="sketch-holder"></div>

Click on the image to give it focus and press the letter keys to create forms in time and space. Each key has a unique identifying number. These numbers can be used to position shapes in space.

.. code:: python

	from p5 import *

	rectWidth = 0

	def setup():
		size(640, 360)
		no_stroke()
		background(0)

		global rectWidth
		rectWidth = width/4

	def draw():
		pass

	def key_pressed():
		keyIndex = -1
		global rectWidth

		if key >= 'A'and key <= 'Z':
			keyIndex = key - 'A'
		elif key >= 'a' and key <= 'z':
			keyIndex = key - 'a'

		if keyIndex == -1:
			# If it's not a letter key, clear the screen
			background(0)
		else:
			fill(millis() % 255)
			x = remap(keyIndex, [0, 25], [0, width - rectWidth])
			rect((x, 0), rectWidth, height)

	if __name__ == '__main__':
		run()