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
      background(127);
      noStroke();
      for (let i = 0; i < height; i += 20) {
        fill(129, 206, 15);
        rect(0, i, width, 10);
        fill(255);
        rect(i, 0, 10, height);
      }
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
