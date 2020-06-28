***************
Color Variables
***************

.. raw:: html

  <script>
	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
	  noStroke();
	  background(51, 0, 0);

	  let inside = color(204, 102, 0);
	  let middle = color(204, 153, 0);
	  let outside = color(153, 51, 0);

	  // These statements are equivalent to the statements above.
	  // Programmers may use the format they prefer.
	  //let inside = color('#CC6600');
	  //let middle = color('#CC9900');
	  //let outside = color('#993300');

	  push();
	  translate(80, 80);
	  fill(outside);
	  rect(0, 0, 200, 200);
	  fill(middle);
	  rect(40, 60, 120, 120);
	  fill(inside);
	  rect(60, 90, 80, 80);
	  pop();

	  push();
	  translate(360, 80);
	  fill(inside);
	  rect(0, 0, 200, 200);
	  fill(outside);
	  rect(40, 60, 120, 120);
	  fill(middle);
	  rect(60, 90, 80, 80);
	  pop();
	}
  </script>
  <div id="sketch-holder"></div>

This example creates variables for colors that may be referred to in the program by a name, rather than a number.

.. code:: python

	from p5 import *

	def setup():
		size(640, 360)

	def draw():
	    no_stroke()

	    bg_col = Color(51, 0, 0)
	    col_1 = Color(204, 102, 0)
	    col_2 = Color(204, 153, 0)
	    col_3 = Color(153, 51, 0)

	    background(bg_col)

	    translate(50, 50)
	    fill(col_3)
	    rect((0, 0), 200, 200)
	    fill(col_2)
	    rect((40, 60), 120, 120)
	    fill(col_1)
	    rect((60, 90), 80, 80)

	    translate(250, 0)
	    fill(col_1)
	    rect((0, 0), 200, 200)
	    fill(col_3)
	    rect((40, 60), 120, 120)
	    fill(col_2)
	    rect((60, 90), 80, 80)

	if __name__ == '__main__':
	  run()

