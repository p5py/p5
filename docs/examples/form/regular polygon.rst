***************
Regular Polygon
***************

.. raw:: html

	<script>

	function setup() {
		var canvas = createCanvas(720, 400);
  	  	canvas.parent('sketch-holder');
	}

	function draw() {
		background(102);

		push();
		translate(width * 0.2, height * 0.5);
		rotate(frameCount / 200.0);
		polygon(0, 0, 82, 3);
		pop();

		push();
		translate(width * 0.5, height * 0.5);
		rotate(frameCount / 50.0);
		polygon(0, 0, 80, 20);
		pop();

		push();
		translate(width * 0.8, height * 0.5);
		rotate(frameCount / -100.0);
		polygon(0, 0, 70, 7);
		pop();
	}

	function polygon(x, y, radius, npoints) {
		let angle = TWO_PI / npoints;
		beginShape();
		for (let a = 0; a < TWO_PI; a += angle) {
			let sx = x + cos(a) * radius;
			let sy = y + sin(a) * radius;
			vertex(sx, sy);
		}
		endShape(CLOSE);
	}

	</script>
	<div id="sketch-holder"></div>

What is your favorite? Pentagon? Hexagon? Heptagon? No? What about the icosagon? The polygon() function created for this example is capable of drawing any regular polygon. Try placing different numbers into the polygon() function calls within draw() to explore.

.. code:: python

	from p5 import *

	def setup():
		size(640, 360)

	def draw():
		background(102)

		with push_matrix():
			translate(width*0.2, height*0.5)
			rotate(frame_count / 200.0)
			polygon(0, 0, 82, 3) # Triangle

		with push_matrix():
			translate(width*0.5, height*0.5)
			rotate(frame_count / 50.0)
			polygon(0, 0, 80, 20)


		with push_matrix():
			translate(width*0.8, height*0.5)
			rotate(frame_count / -100.0)
			polygon(0, 0, 70, 7)

	def polygon(x, y, radius, npoints):
		angle = TWO_PI / npoints

		begin_shape()
		a = 0
		while a < TWO_PI:
			sx = x + cos(a)*radius
			sy = y + sin(a)*radius
			vertex(sx, sy)

			a = a + angle

		end_shape()


	if __name__ == '__main__':
		run()