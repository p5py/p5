**********
Alpha Mask
**********

.. raw:: html

    <script>
	let img;
	let imgMask;

	function preload() {
		img = loadImage('https://p5js.org/assets/examples/assets/moonwalk.jpg');
		imgMask = loadImage('https://p5js.org/assets/examples/assets/mask.png');
	}

	function setup() {
		var canvas = createCanvas(720, 400);
        canvas.parent('sketch-holder');
		img.mask(imgMask);
		imageMode(CENTER);
	}

	function draw() {
		background(0, 102, 153);
		image(img, width / 2, height / 2);
		image(img, mouseX, mouseY);
	}

    </script>
    <div id="sketch-holder"></div>


Loads a "mask" for an image to specify the transparency in different parts of the image. The two images are blended together using the ``mask()`` method of p5.Image.


.. code:: python

	from p5 import *

	img = None
	imgMask = None

	def setup():
	    global img
	    size(720, 400)
	    img = load_image("moonwalk.jpg")
	    imgMask = load_image("mask.png")

	    img.mask(imgMask)
	    imageMode("CENTER")

	def draw():
	    global img
	    background(0, 102, 153)
	    image(img, (width / 2, height / 2))
	    image(img, mouse_x, mouse_y)

	if __name__ == '__main__':
	    run()