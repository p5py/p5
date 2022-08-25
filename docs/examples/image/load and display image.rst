****************
Load and Display 
****************

.. raw:: html

    <script>
    let img; // Declare variable 'img'.

    function setup() {
        var canvas = createCanvas(720, 400);
        canvas.parent('sketch-holder');
        img = loadImage('https://p5js.org/assets/examples/assets/moonwalk.jpg'); // Load the image
    }

    function draw() {
        // Displays the image at its actual size at point (0,0)
        image(img, 0, 0);
        // Displays the image at point (0, height/2) at half size
        image(img, 0, height / 2, img.width / 2, img.height / 2);
    }

    </script>
    <div id="sketch-holder"></div>


Images can be loaded and displayed to the screen at their actual size or any other size.

.. code:: python

    from p5 import *

    img = None

    def setup():
        global img
        size(720, 400)
        img = load_image("moonwalk.jpg")

    def draw():
        global img
        background(0)
        image(img, 0, 0)
        image(img, 0, height / 2, img.width / 2, img.height / 2)

    if __name__ == '__main__':
        run()