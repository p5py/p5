****
Loop
****

.. raw:: html

  <script>
  let y = 100;

  // The statements in the setup() function
  // execute once when the program begins
  function setup() {
    var canvas = createCanvas(720, 400);
    canvas.parent('sketch-holder');
    stroke(255); // Set line drawing color to white
    frameRate(30);
  }
  // The statements in draw() are executed until the
  // program is stopped. Each statement is executed in
  // sequence and after the last line is read, the first
  // line is executed again.
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


The ``loop()`` function causes ``draw()`` to execute continuously. If noLoop is called in ``setup()`` the ``draw()`` is only executed once. In this example click the mouse to execute ``loop()``, which will cause the ``draw()`` the execute continuously.

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

  def mouse_pressed():
    loop()

  if __name__ == '__main__':
    run()
