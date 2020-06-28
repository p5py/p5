from p5 import *

def setup():
    size(720, 400)

def draw():
    offset = 0
    x = 0
    while x < 2 * PI:
        arc((50.0 + offset, 50.0), 50.0, 50.0, x, 2 * PI)
        arc((50.0 + offset, 100), 50, 50, x, 2 * PI, 'OPEN')
        arc((50.0 + offset, 150), 50, 50, x, 2 * PI, 'CHORD')
        arc((50.0 + offset, 200), 50, 50, x, 2 * PI, 'PIE')
        x += QUARTER_PI
        offset += 50

    # no_fill()
    # begin_shape()
    # curve_vertex(84, 91)
    # curve_vertex(84, 91)
    # curve_vertex(68, 19)
    # curve_vertex(21, 17)
    # curve_vertex(32, 100)
    # curve_vertex(32, 100)
    # end_shape()

# Bezier_vertex 1
#     no_fill()
#     begin_shape()
#     vertex(30, 20)
#     bezier_vertex(80, 0, 80, 75, 30, 75)
#     end_shape()

# Bezier vertex 2
#     begin_shape()
#     vertex(30, 20)
#     bezier_vertex(80, 0, 80, 75, 30, 75)
#     bezier_vertex(50, 80, 60, 25, 30, 20)
#     end_shape()
#     no_loop()

if __name__ == '__main__':
    run()
