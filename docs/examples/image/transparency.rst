************
Transparency
************

.. raw:: html

    <script>
	let img;
	let offset = 0;
	let easing = 0.05;

	function setup() {
		var canvas = createCanvas(720, 400);
        canvas.parent('sketch-holder');
		img = loadImage('https://p5js.org/assets/examples/assets/moonwalk.jpg'); // Load an image into the program
	}

	function draw() {
		image(img, 0, 0); // Display at full opacity
		let dx = mouseX - img.width / 2 - offset;
		offset += dx * easing;
		tint(255, 127); // Display at half opacity
		image(img, offset, 0);
	}
    </script>
    <div id="sketch-holder"></div>


Move the pointer left and right across the image to change its position. This program overlays one image over another by modifying the alpha value of the image with the ``tint()`` function.


.. code:: python

	from p5 import *

	img = None
	offset = 0
	easing = 0.05

	def setup():
		global img
		size(720, 400)
		img = load_image("moonwalk.jpg")

	def draw():
		global img, offset, easing

		image(img, (0, 0)) #Display at full opacity

		dx = mouse_x - img.width / 2 - offset
		offset += dx * easing
		tint(255, 127)
		image(img, (offset, 0))

	if __name__ == '__main__':
		run()