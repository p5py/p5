from p5 import *

x = 0
y = 0
easing = 0.05

def setup():
        size(640, 360)
        no_stroke()

def draw():
        background(100, 10, 20)

        global x, y, easing
        targetX = mouse_x
        dx = targetX - x
        x += dx * easing

        targetY = mouse_y
        dy = targetY - y
        y += dy * easing

        ellipse((x, y), 66, 66)

if __name__ == '__main__':
        run()