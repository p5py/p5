from p5 import *


def setup():
    size(720, 400)


def draw():
    no_fill()
    begin_shape()
    vertex(30, 20)
    bezier_vertex(80, 0, 80, 75, 30, 75)
    end_shape()

    fill('white')
    begin_shape()
    vertex(130, 20)
    bezier_vertex(180, 0, 180, 75, 130, 75)
    bezier_vertex(150, 80, 160, 25, 130, 20)
    end_shape()

    begin_shape()
    curve_vertex(284, 91)
    curve_vertex(284, 91)
    curve_vertex(268, 19)
    curve_vertex(221, 17)
    curve_vertex(232, 91)
    curve_vertex(232, 91)
    end_shape()

    begin_shape()
    vertex(20, 120)
    quadratic_vertex(80, 120, 50, 150)
    end_shape()

    begin_shape()
    vertex(120, 120)
    quadratic_vertex(180, 120, 150, 150)
    quadratic_vertex(120, 180, 180, 180)
    vertex(180, 160)
    end_shape()


if __name__ == '__main__':
    run()
