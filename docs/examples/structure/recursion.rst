*********
Recursion
*********

.. raw:: html

  <script>
  function setup() {
  var canvas = createCanvas(720, 400);
  canvas.parent('sketch-holder');
    noStroke();
    noLoop();
  }

  function draw() {
    drawCircle(width / 2, 280, 6);
  }

  function drawCircle(x, radius, level) {
    const tt = (126 * level) / 4.0;
    fill(tt);
    ellipse(x, height / 2, radius * 2, radius * 2);
    if (level > 1) {
      level = level - 1;
      drawCircle(x - radius / 2, radius / 2, level);
      drawCircle(x + radius / 2, radius / 2, level);
    }
  }
  </script>
  <div id="sketch-holder"></div>


A demonstration of recursion, which means functions call themselves. Notice how the ``drawCircle()`` function calls itself at the end of its block. It continues to do this until the variable ``level`` is equal to 1.

.. code:: python

  from p5 import *

  def setup():
  	size(640, 360)
  	no_stroke()
  	no_loop()

  def draw():
  	drawCircle(width/2, 280, 6)

  def drawCircle(x, radius, level):
  	tt = 126*level/4.0
  	fill(tt)
  	ellipse((x, height/2), radius*2, radius*2)
  	if level > 1:
  		level = level - 1
  		drawCircle(x - radius/2, radius/2, level)
  		drawCircle(x + radius/2, radius/2, level)

  if __name__ == '__main__':
      run()
