from p5 import *

x = 0
y = 0
angle1 = 0.0
angle2 = 0.0
segLength = 100

def setup():
        size(640, 360)
        stroke(255, 160)
        stroke_weight(30)

        global x, y
        x = width * 0.3
        y = height * 0.5

def draw():
        x = width * 0.3
        y = height * 0.5
        
        background(0)

        angle1 = (mouse_x/width - 0.5) * -PI
        angle2 = (mouse_y/height - 0.5) * PI

        with push_matrix():
                segment(x, y, angle1)
                segment(segLength, 0, angle2)

def segment(x, y, a):
        translate(x, y)
        rotate(a)
        line((0, 0), (segLength, 0))

if __name__ == '__main__':
  run()