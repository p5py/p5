from p5 import *

x = 0
y = 0
dim = 80.0

def setup():
        size(640, 360)
        no_stroke()

def draw():
        background(102)

        global x
        x = x + 0.8

        if x > width + dim:
                x = -dim

        translate(x, height/2 - dim/2)
        fill(255)
        rect((-dim/2, -dim/2), dim, dim)

        # Transforms accumulate. Notice how this rect moves
        # twice as fast as the other, but it has the same
        # parameter for the x-axis value
        translate(x, dim)
        fill(0)
        rect((-dim/2, -dim/2), dim, dim)

if __name__ == '__main__':
        # run(renderer='skia')
        print("Translate not implemented yet")
