*******
Letters
*******

.. raw:: html

  	<script>
	let font,
	fontsize = 32;

	function preload() {
		// Ensure the .ttf or .otf font stored in the assets directory
		// is loaded before setup() and draw() are called
		font = loadFont('https://p5js.org/assets/examples/assets/SourceSansPro-Regular.otf');
	}

	function setup() {
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');

		// Set text characteristics
		textFont(font);
		textSize(fontsize);
		textAlign(CENTER, CENTER);
	}

	function draw() {
		background(160);

		// Set the gap between letters and the left and top margin
		let gap = 52;
		let margin = 10;
		translate(margin * 4, margin * 4);

		// Set the counter to start at the character you want
		// in this case 35, which is the # symbol
		let counter = 35;

		// Loop as long as there is space on the canvas
		for (let y = 0; y < height - gap; y += gap) {
		for (let x = 0; x < width - gap; x += gap) {
			// Use the counter to retrieve individual letters by their Unicode number
			let letter = char(counter);

			// Add different color to the vowels and other characters
			if (
				letter === 'A' ||
				letter === 'E' ||
				letter === 'I' ||
				letter === 'O' ||
				letter === 'U'
				) {
				fill('#ed225d');
			} else {
				fill(255);
			}

			// Draw the letter to the screen
			text(letter, x, y);

			// Increment the counter
			counter++;
			}
		}
	}
  	</script>
  	<div id="sketch-holder"></div>

Draws letters to the screen. This requires loading a font, setting the font, and then drawing the letters.


.. code:: python

	from p5 import *

	f = None

	def setup():
		global f
		size(640, 360)
		background(0)

		# Create the font
		f = create_font("Arial.ttf", 16)
		text_font(f)
		text_align("CENTER")

	def draw():
		background(0)
		
		# Set the left and top margin
		margin = 10
		translate(margin*4, margin*4)

		gap = 46
		counter = 35

		for y in range(0, height - gap, gap):
			for x in range(0, width - gap, gap):

				letter = chr(counter)
				
				if (letter == "A" or letter == "E" or letter == "I" or letter == "0" or letter == "U"):
					fill(255, 204, 0)
				else:
					fill(255)

				# Draw the letter to the screen
				text(letter, (x, y))

				# Increment the counter
				counter += 1

	if __name__ == '__main__':
		run()
