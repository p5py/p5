***************
Create Graphics
***************

.. raw:: html

    <script>

    let pg;

    function setup() {
      var canvas = createCanvas(710, 400);
      canvas.parent('sketch-holder');
      pg = createGraphics(400, 250);
    }

    function draw() {
      fill(0, 12);
      rect(0, 0, width, height);
      fill(255);
      noStroke();
      ellipse(mouseX, mouseY, 60, 60);

      pg.background(51);
      pg.noFill();
      pg.stroke(255);
      pg.ellipse(mouseX - 150, mouseY - 75, 60, 60);

      //Draw the offscreen buffer to the screen with image()
      image(pg, 150, 75);
    }
    </script>
    <div id="sketch-holder"></div>


The ``draw_target()`` function makes it easy to draw many distinct targets. Each call to ``draw_target()`` specifies the position, size, and number of rings for each target.

.. code:: python

    from p5 import *

    pg = None

    def setup():
        global pg
        size(710, 400)
        pg = create_graphics(400,250)

    def draw():
        fill(0, 12)
        rect(0, 0, width, height)
        fill(255)
        no_stroke()
        ellipse(mouse_x, mouse_y, 60, 60)

        pg.background(51)
        pg.no_fill()
        pg.stroke(255)
        pg.ellipse(mouse_x - 150, mouse_y - 75, 60, 60)

        # Draw the offscreen buffer to the screen with image()
        image(pg, 150, 75)

    if __name__ == '__main__':
          # Create Graphics is only available in skia
          run(renderer='skia')
