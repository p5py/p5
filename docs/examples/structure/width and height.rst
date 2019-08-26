****************
Width and Height
****************


.. raw:: html

  <script>
    function setup() {
      var canvas = createCanvas(720, 400);
      canvas.parent('sketch-holder');
    }

    function draw() {
    // Set the background to black and turn off the fill color
    background(0);
    noFill();

    // The two parameters of the point() method each specify
    // coordinates.
    // The first parameter is the x-coordinate and the second is the Y
    stroke(255);
    point(width * 0.5, height * 0.5);
    point(width * 0.5, height * 0.25);

    // Coordinates are used for drawing all shapes, not just points.
    // Parameters for different functions are used for different
    // purposes. For example, the first two parameters to line()
    // specify the coordinates of the first endpoint and the second
    // two parameters specify the second endpoint
    stroke(0, 153, 255);
    line(0, height * 0.33, width, height * 0.33);

    // By default, the first two parameters to rect() are the
    // coordinates of the upper-left corner and the second pair
    // is the width and height
    stroke(255, 153, 0);
    rect(width * 0.25, height * 0.1, width * 0.5, height * 0.8);
    }
    </script>
    <div id="sketch-holder"></div>


The ``width`` and ``height`` variables contain the width and height of the display window as defined in the ``size()`` function.

.. code:: python

	from p5 import *

	def setup():
		size(640, 360)

	def draw():
		background(127)
		no_stroke()

		for i in range(0, height, 20):
			fill(129, 206, 15)
			rect((0, i), width, 10)
			fill(255)
			rect((i, 0), 10, height)

	if __name__ == '__main__':
	    run()
