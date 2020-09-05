from p5 import *


def setup():
    size(640, 360)
    no_loop()


def draw():
    translate(50, 50)
    stroke(255, 0, 0)
    begin_shape()
    # Exterior part of shape, clockwise winding
    vertex(-40, -40)
    vertex(40, -40)
    vertex(40, 40)
    vertex(-40, 40)
    # # Interior part of shape, counter-clockwise winding
    begin_contour()
    vertex(-20, -20)
    vertex(-20, 20)
    vertex(20, 20)
    vertex(20, -20)
    end_contour()
    end_shape('CLOSE')


run(mode="P2D")
