from p5 import *


def setup():
    size(640, 360)
    stroke(255)
    no_stroke()


def draw():
    if frame_count > 30:
        exit()
    background(51)
    draw_target(width * 0.25, height * 0.4, 200, 4)
    draw_target(width * 0.5, height * 0.5, 300, 10)
    draw_target(width * 0.75, height * 0.3, 120, 6)


def draw_target(xloc, yloc, size, num):
    grayvalues = 255 / num
    steps = size / num
    for i in range(num):
        fill(i * grayvalues)
        ellipse((xloc, yloc), size - i * steps, size - i * steps)
