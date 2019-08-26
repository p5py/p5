****************
Background Image 
****************

.. raw:: html

    <script>
    let bg;
    let y = 0;

    function setup() {
        // The background image must be the same size as the parameters
        // into the createCanvas() method. In this program, the size of
        // the image is 720x400 pixels.
        bg = loadImage('https://p5js.org/assets/examples/assets/moonwalk.jpg');
        var canvas = createCanvas(720, 400);
        canvas.parent('sketch-holder');
    }

    function draw() {
        background(bg);

        stroke(226, 204, 0);
        line(0, y, width, y);

        y++;
        if (y > height) {
            y = 0;
        }
    }
    </script>
    <div id="sketch-holder"></div>


This example presents the fastest way to load a background image. To load an image as the background, it must be the same width and height as the program.

.. code:: python

    from p5 import *

    bg = None
    y = 0

    def setup():
        global bg
        size(720, 400)
        bg = load_image("moonwalk.jpg")

    def draw():
        global img, y
        background(bg)

        stroke(226, 204, 0)
        line((0, y), (width, y))

        y += 1

        if y > height:
            y = 0

    if __name__ == '__main__':
        run()