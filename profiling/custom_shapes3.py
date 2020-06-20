from p5 import *

x = 0
y = 0
outsideRadius = 150
insideRadius = 100

def setup():
        size(720, 400)
        background(204)

        global x, y
        x = width / 2
        y = height / 2

def draw():
        # begin_shape('TRIANGLES')
        # vertex(30, 75)
        # vertex(40, 20)
        # vertex(50, 75)
        # vertex(60, 20)
        # vertex(70, 75)
        # vertex(80, 20)
        # end_shape()

        # begin_shape('TRIANGLE_FAN')
        # vertex(57.5, 50)
        # vertex(57.5, 15)
        # vertex(92, 50)
        # vertex(57.5, 85)
        # vertex(22, 50)
        # vertex(57.5, 15)
        # end_shape()

        begin_shape('QUAD_STRIP')
        vertex(30, 20)
        vertex(30, 75)
        vertex(50, 20)
        vertex(50, 75)
        vertex(65, 20)
        vertex(65, 75)
        vertex(85, 20)
        vertex(85, 75)
        end_shape()

        # begin_shape('QUADS')
        # vertex(30, 20)
        # vertex(30, 75)
        # vertex(50, 75)
        # vertex(50, 20)
        # vertex(65, 20)
        # vertex(65, 75)
        # vertex(85, 75)
        # vertex(85, 20)
        # end_shape()

if __name__ == '__main__':
        run()
