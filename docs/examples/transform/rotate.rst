******
Rotate
******

.. raw:: html

  <script>
	let angle = 0.0;
	let jitter = 0.0;

	function setup() {
	  var canvas = createCanvas(720, 400);
  	  canvas.parent('sketch-holder');
  	  noStroke();
	  fill(255);
	  //Draw the rectangle from the center and it will also be the
	  //rotate around that center
	  rectMode(CENTER);
	}

	function draw() {
	  background(51);

	  // during even-numbered seconds (0, 2, 4, 6...) add jitter to
	  // the rotation
	  if (second() % 2 === 0) {
	    jitter = random(-0.1, 0.1);
	  }
	  //increase the angle value using the most recent jitter value
	  angle = angle + jitter;
	  //use cosine to get a smooth CW and CCW motion when not jittering
	  let c = cos(angle);
	  //move the shape to the center of the canvas
	  translate(width / 2, height / 2);
	  //apply the final rotation
	  rotate(c);
	  rect(0, 0, 180, 180);
	}
  </script>
  <div id="sketch-holder"></div>

Rotating a square around the Z axis. To get the results you expect, send the rotate function angle parameters that are values between 0 and PI*2 (TWO_PI which is roughly 6.28). If you prefer to think about angles as degrees (0-360), you can use the radians() method to convert your values. For example: scale(radians(90)) is identical to the statement scale(PI/2).


.. code:: python

	from p5 import *

	angle = 0.0
	jitter = 0.0

	def setup():
		size(640, 360)
		fill(255) 	
		no_stroke()	  

	def draw():
		background(102)

		global angle
		global jitter

		if second()%2 == 0:
			jitter = random_uniform(-0.1, 0.1)
		
		angle = angle + jitter
		c = cos(angle)
		translate(width/2, height/2)
		rotate(c)
		rect((-90, -90), 180, 180)

	if __name__ == '__main__':
	  run()
