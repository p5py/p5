from p5 import *


def setup():
    size(640, 360)
    no_stroke()
    rect_mode("CENTER")


def draw():
    background(230)

    background(51)
    fill(255, 204)
    rect((mouse_x, height / 2), mouse_y / 2 + 10, mouse_y / 2 + 10)

    fill(255, 204)
    inverseX = width - mouse_x
    inverseY = height - mouse_y
    rect((inverseX, height / 2), (inverseY / 2) + 10, (inverseY / 2) + 10)
