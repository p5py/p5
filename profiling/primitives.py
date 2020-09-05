from p5 import *


def setup():
    size(720, 400)


def draw():
    triangle((30, 75), (58, 20), (86, 75))
    square((130, 20), 55)
    rect((230, 20), 55, 25)
    quad((38, 131), (86, 120), (69, 163), (30, 176))
    line((130, 120), (185, 175))
    ellipse((256, 146), 35, 55)
    circle((56, 246), 55)


if __name__ == '__main__':
    run()
