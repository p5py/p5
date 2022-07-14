from p5 import *


def setup():
    size(640, 360)


def draw():
    background(102)

    with push_matrix():
        translate(width * 0.2, height * 0.5)
        rotate(frame_count / 200.0)
        star(0, 0, 5, 70, 3)

    with push_matrix():
        translate(width * 0.5, height * 0.5)
        rotate(frame_count / 400.0)
        star(0, 0, 80, 100, 40)

    with push_matrix():
        translate(width * 0.8, height * 0.5)
        rotate(frame_count / -100.0)
        star(0, 0, 30, 70, 5)


def star(x, y, radius1, raduis2, npoints):
    angle = TWO_PI / npoints
    half_angle = angle / 2.0

    begin_shape()
    a = 0
    while a < TWO_PI:
        sx = x + cos(a) * raduis2
        sy = y + sin(a) * raduis2
        vertex(sx, sy)
        sx = x + cos(a + half_angle) * radius1
        sy = y + sin(a + half_angle) * radius1
        vertex(sx, sy)
        a = a + angle

    end_shape()
