from p5 import *

angle = 0.0
jitter = 0.0

def setup():
        size(640, 360)
        fill(255)
        no_stroke()

def draw():
        background(102)

        global angle
        global jitter

        if second()%2 == 0:
                jitter = random_uniform(-0.1, 0.1)

        angle = angle + jitter
        c = cos(angle)
        translate(width/2, height/2)
        rotate(c)
        rect((-90, -90), 180, 180)

if __name__ == '__main__':
  run()