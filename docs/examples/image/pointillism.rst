***********
Pointillism 
***********

.. raw:: html

    <script>
    let img;
    let smallPoint, largePoint;

    function preload() {
        img = loadImage('https://p5js.org/assets/examples/assets/moonwalk.jpg');
    }

    function setup() {
        var canvas = createCanvas(720, 400);
        canvas.parent('sketch-holder');
        smallPoint = 4;
        largePoint = 40;
        imageMode(CENTER);
        noStroke();
        background(255);
        img.loadPixels();
    }

    function draw() {
        let pointillize = map(mouseX, 0, width, smallPoint, largePoint);
        let x = floor(random(img.width));
        let y = floor(random(img.height));
        let pix = img.get(x, y);
        fill(pix, 128);
        ellipse(x, y, pointillize, pointillize);
    }

    </script>
    <div id="sketch-holder"></div>

By Dan Shiffman. Mouse horizontal location controls size of dots. Creates a simple pointillist effect using ellipses colored according to pixels in an image.

.. code:: python

    from p5 import *

    img = None
    small_point = 4
    large_point = 40

    def setup():
        global img
        size(720, 400)
        no_stroke()
        background(255)
        img = load_image("moonwalk.jpg")


    def draw():
        global img, large_point, small_point
        pointillize = remap(mouse_x, [0, width], [small_point, large_point])
        x = floor(random_uniform(img.width))
        y = floor(random_uniform(img.height))

        pix = img._get_pixel((x, y))
        fill(pix, 128)

        ellipse((x, y), pointillize, pointillize)

    if __name__ == '__main__':
        run()