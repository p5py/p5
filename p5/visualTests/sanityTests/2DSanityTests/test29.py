from p5 import *

num = 60
mx = [0] * num
my = [0] * num


def setup():
    size(640, 360)
    no_stroke()
    fill(255, 153)


def draw():
    background(51)

    global num, mx, my

    which = frame_count % num

    mx[which] = mouse_x
    my[which] = mouse_y

    for i in range(num):
        index = (which + 1 + i) % num
        ellipse([mx[index], my[index]], i, i)
