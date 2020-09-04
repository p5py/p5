from p5 import *


def setup():
    size(640, 360)
    no_loop()


def draw():
    background(0)

    stroke(255)
    rotate_x(PI * 3 / 2)
    rotate_z(PI / 6)
    fill(255)
    begin_shape()
    vertex(-100, -100, -100)
    vertex(100, -100, -100)
    vertex(0, 0, 100)

    vertex(100, -100, -100)
    vertex(100, 100, -100)
    vertex(0, 0, 100)

    vertex(100, 100, -100)
    vertex(-100, 100, -100)
    vertex(0, 0, 100)

    vertex(-100, 100, -100)
    vertex(-100, -100, -100)
    vertex(0, 0, 100)
    end_shape()


run(mode='P3D')
