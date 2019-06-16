************
Milliseconds
************

.. raw:: html

  <script>
	
  </script>
  <div id="sketch-holder"></div>

A millisecond is 1/1000 of a second. Processing keeps track of the number of milliseconds a program has run. By modifying this number with the modulo(%) operator, different patterns in time are created.


.. code:: python

	from p5 import *

	scale = 0

	def setup():
		size(640, 360)
		no_stroke()

		global scale
		scale = width/20

	def draw():
		global scale
		for i in range(int(scale)):
			color_mode("RGB", (i+1) * scale * 10)
			fill(millis()%((i+1) * scale * 10))
			rect([i*scale, 0], scale, height)


	if __name__ == '__main__':
		run()