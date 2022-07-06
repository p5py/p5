from p5 import *

a = 0.0
s = 0.0

def setup():
        size(640, 360)
        no_stroke()

def draw():
        background(102)

        global a
        global s

        a = a + 0.04
        s = cos(a)*2

        translate(width/2, height/2)
        scale(s)
        fill(51)
        rect((-25, -25), 50, 50)

        translate(75, 0)
        fill(255)
        scale(s)
        rect((-25, -25), 50, 50)

if __name__ == '__main__':
        run()