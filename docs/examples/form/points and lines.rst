****************
Points and Lines
****************

.. raw:: html

	<script>

	function setup() {
		let d = 70;
		let p1 = d;
		let p2 = p1 + d;
		let p3 = p2 + d;
		let p4 = p3 + d;

		// Sets the screen to be 720 pixels wide and 400 pixels high
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
		background(0);
		noSmooth();

		translate(140, 0);

		// Draw gray box
		stroke(153);
		line(p3, p3, p2, p3);
		line(p2, p3, p2, p2);
		line(p2, p2, p3, p2);
		line(p3, p2, p3, p3);

		// Draw white points
		stroke(255);
		point(p1, p1);
		point(p1, p3);
		point(p2, p4);
		point(p3, p1);
		point(p4, p2);
		point(p4, p4);
	}

	</script>
	<div id="sketch-holder"></div>

Points and lines can be used to draw basic geometry. Change the value of the variable ``d`` to scale the form. The four variables set the positions based on the value of ``d``.

.. code:: python

	from p5 import *

	def setup():
		# Sets the screen to be 720 pixels wide and 400 pixels high
		size(720, 400)
		no_loop()

	def draw():
		d = 70
		p1 = d
		p2 = p1 + d
		p3 = p2 + d
		p4 = p3 + d

		background(0)
		no_smooth()

		translate(140, 0)

		# Draw gray box
		stroke(153)
		line((p3, p3), (p2, p3))
		line((p2, p3), (p2, p2))
		line((p2, p2), (p3, p2))
		line((p3, p2), (p3, p3))

		# Draw white points
		stroke(255)
		point(p1, p1)
		point(p1, p3)
		point(p2, p4)
		point(p3, p1)
		point(p4, p2)
		point(p4, p4)

	if __name__ == '__main__':
		run()