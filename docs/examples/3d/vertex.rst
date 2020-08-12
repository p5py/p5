************
Vertex
************

.. raw:: html

    <script>
    function setup() {
        let canvas = createCanvas(720, 400, WEBGL);
        canvas.parent('sketch-holder');
    }

    function draw() {
        background(0);

        stroke(255);
        rotateX(PI/2);
        rotateZ(-PI/6);
        noFill();

        beginShape();
        vertex(-50, -50, -50);
        vertex( 50, -50, -50);
        vertex(   0,    0,  50);

        vertex( 50, -50, -50);
        vertex( 50,  50, -50);
        vertex(   0,    0,  50);

        vertex( 50, 50, -50);
        vertex(-50, 50, -50);
        vertex(   0,   0,  50);

        vertex(-50,  50, -50);
        vertex(-50, -50, -50);
        vertex(   0,    0,  50);
        endShape();
    }
    </script>
    <div id="sketch-holder"></div>
    <br>


.. code:: python

    # Code from Daniel Shiffman's tutorial, adopted to p5py
    # https://processing.org/tutorials/p3d/

    from p5 import *

    def setup():
        size(640, 360)
        no_loop()

    def draw():
        background(0)

        stroke(255)
        rotate_x(PI*3/2)
        rotate_z(PI/6)
        fill(255)
        begin_shape()
        vertex(-100, -100, -100)
        vertex( 100, -100, -100)
        vertex(   0,    0,  100)

        vertex( 100, -100, -100)
        vertex( 100,  100, -100)
        vertex(   0,    0,  100)

        vertex( 100, 100, -100)
        vertex(-100, 100, -100)
        vertex(   0,   0,  100)

        vertex(-100,  100, -100)
        vertex(-100, -100, -100)
        vertex(   0,    0,  100)
        end_shape()

    run(mode='P3D')
