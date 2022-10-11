from p5 import *


def setup():
    size(300, 300)


def draw():
    # print(width, height)
    circle(mouse_x, mouse_y, 20)


run(renderer="skia")
