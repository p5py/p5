********
Function
********

.. raw:: html

  <script>
  function setup() {
  var canvas = createCanvas(720, 400);
  canvas.parent('sketch-holder');
    background(51);
    noStroke();
    noLoop();
  }

  function draw() {
    drawTarget(width * 0.25, height * 0.4, 200, 4);
    drawTarget(width * 0.5, height * 0.5, 300, 10);
    drawTarget(width * 0.75, height * 0.3, 120, 6);
  }

  function drawTarget(xloc, yloc, size, num) {
    const grayvalues = 255 / num;
    const steps = size / num;
    for (let i = 0; i < num; i++) {
      fill(i * grayvalues);
      ellipse(xloc, yloc, size - i * steps, size - i * steps);
    }
  }
  </script>
  <div id="sketch-holder"></div>


The ``drawTarget()`` function makes it easy to draw many distinct targets. Each call to ``drawTarget()`` specifies the position, size, and number of rings for each target.

.. code:: python

  from p5 import *

  def setup():
  	size(640, 360)
  	stroke(255)
  	no_stroke()

  def draw():
  	background(51)
  	drawTarget(width*0.25, height*0.4, 200, 4)
  	drawTarget(width*0.5, height*0.5, 300, 10)
  	drawTarget(width*0.75, height*0.3, 120, 6)

  def drawTarget(xloc, yloc, size, num):
  	grayvalues = 255/num
  	steps = size/num
  	for i in range(num):
  		fill(i*grayvalues)
  		ellipse((xloc, yloc), size - i*steps, size - i*steps)

  if __name__ == '__main__':
      run()
