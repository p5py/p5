from p5 import *


def setup():
    size(640, 360)


def draw():
    pass
    background(102)

    with push_matrix():
        translate(width * 0.2, height * 0.5)
        rotate(frame_count / 200.0)
        polygon(0, 0, 82, 3)  # Triangle

    with push_matrix():
        translate(width * 0.5, height * 0.5)
        rotate(frame_count / 50.0)
        polygon(0, 0, 80, 20)

    with push_matrix():
        translate(width * 0.8, height * 0.5)
        rotate(frame_count / -100.0)
        polygon(0, 0, 70, 7)


def polygon(x, y, radius, npoints):
    angle = TWO_PI / npoints

    begin_shape()
    a = 0
    while a < TWO_PI:
        sx = x + cos(a) * radius
        sy = y + sin(a) * radius
        vertex(sx, sy)

        a = a + angle

    end_shape()
