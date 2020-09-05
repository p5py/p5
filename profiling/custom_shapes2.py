from p5 import *


def setup():
    size(720, 400)


def draw():
    begin_shape(TRIANGLES)
    vertex(30, 75)
    vertex(40, 20)
    vertex(50, 75)
    vertex(60, 20)
    vertex(70, 75)
    vertex(80, 20)
    end_shape()

    begin_shape(TRIANGLE_FAN)
    vertex(157.5, 50)
    vertex(157.5, 15)
    vertex(192, 50)
    vertex(157.5, 85)
    vertex(122, 50)
    vertex(157.5, 15)
    end_shape()

    begin_shape(QUAD_STRIP)
    vertex(230, 20)
    vertex(230, 75)
    vertex(250, 20)
    vertex(250, 75)
    vertex(265, 20)
    vertex(265, 75)
    vertex(285, 20)
    vertex(285, 75)
    end_shape()

    begin_shape(QUADS)
    vertex(330, 20)
    vertex(330, 75)
    vertex(350, 75)
    vertex(350, 20)
    vertex(365, 20)
    vertex(365, 75)
    vertex(385, 75)
    vertex(385, 20)
    end_shape()

    begin_shape(LINES)
    vertex(30, 120)
    vertex(85, 120)
    vertex(85, 175)
    vertex(30, 175)
    end_shape()

    no_fill()
    begin_shape()
    vertex(130, 120)
    vertex(185, 120)
    vertex(185, 175)
    vertex(130, 175)
    end_shape()

    begin_shape()
    vertex(230, 120)
    vertex(285, 120)
    vertex(285, 175)
    vertex(230, 175)
    end_shape(CLOSE)
    fill(255, 255, 255)

    begin_shape(TRIANGLE_STRIP)
    vertex(330, 175)
    vertex(340, 120)
    vertex(350, 175)
    vertex(360, 120)
    vertex(370, 175)
    vertex(380, 120)
    vertex(390, 175)
    end_shape()

    begin_shape()
    vertex(20, 220)
    vertex(40, 220)
    vertex(40, 240)
    vertex(60, 240)
    vertex(60, 260)
    vertex(20, 260)
    end_shape(CLOSE)


if __name__ == '__main__':
    run()
