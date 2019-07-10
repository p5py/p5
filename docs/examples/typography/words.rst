*****
Words
*****

.. raw:: html

  	<script>
	let font,
	fontsize = 40;

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

		// Align the text to the right
		// and run drawWords() in the left third of the canvas
		textAlign(RIGHT);
		drawWords(width * 0.25);

		// Align the text in the center
		// and run drawWords() in the middle of the canvas
		textAlign(CENTER);
		drawWords(width * 0.5);

		// Align the text to the left
		// and run drawWords() in the right third of the canvas
		textAlign(LEFT);
		drawWords(width * 0.75);
	}

	function drawWords(x) {
		// The text() function needs three parameters:
		// the text to draw, the horizontal position,
		// and the vertical position
		fill(0);
		text('ichi', x, 80);

		fill(65);
		text('ni', x, 150);

		fill(190);
		text('san', x, 220);

		fill(255);
		text('shi', x, 290);
	}

  	</script>
  	<div id="sketch-holder"></div>

The ``text()`` function is used for writing words to the screen. The letters can be aligned left, center, or right with the textAlign() function.

.. code:: python

	from p5 import *

	f = None

	def setup():
		global f
		size(640, 360)

		# Create the font
		f = create_font("Arial.ttf", 16)
		text_font(f)
		text_align("CENTER")

	def draw():
		background(102)
		text_align("RIGHT")
		drawType(width * 0.25)
		text_align("CENTER")
		drawType(width * 0.5)
		text_align("LEFT")
		drawType(width * 0.75)

	def drawType(x):
		line((x, 0), (x, 65))
		line((x, 220), (x, height))
		fill(0)
		text("ichi", (x, 95))
		fill(51)
		text("ni", (x, 130))
		fill(204)
		text("san", (x, 165))
		fill(255)
		text("shi", (x, 210))

	if __name__ == '__main__':
		run()