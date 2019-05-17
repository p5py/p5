*******
No Loop
*******

.. raw:: html

  <script>
		let y;
    function setup() {
      var canvas = createCanvas(720, 400);
			canvas.parent('sketch-holder');

      stroke(255); // Set line drawing color to white
      noLoop();

      y = height * 0.5;
    }

    function draw() {
      background(0); // Set the background to black
      y = y - 1;
      if (y < 0) {
        y = height;
      }
      line(0, y, width, y);
    }
  </script>
  <div id="sketch-holder"></div>


The ``no_loop()`` function causes ``draw()`` to only execute once. Without calling ``no_loop()``, the code inside ``draw()`` is run continually.


.. code:: python

  from p5 import *

  y = 0

  # The statements in the setup() function
  # run once when the program begins
  def setup():
    size(640, 360)  # Size should be the first statement
    stroke(255)     # Set stroke color to white
    no_loop()

    global y
    y = height * 0.5

  # The statements in draw() are executed until the
  # program is stopped. Each statement is executed in
  # sequence and after the last line is read, the first
  # line is executed again.
  def draw():
    background(0) # Set the background to black
    global y
    y = y - 1
    if y < 0:
      y = height

    line((0, y), (width, y))


  if __name__ == '__main__':
    run()
