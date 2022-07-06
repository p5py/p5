from p5 import *

def setup():
        # Sets the screen to be 720 pixels wide and 400 pixels high
        size(720, 400)
        no_loop()

def draw():
        d = 70
        p1 = d
        p2 = p1 + d
        p3 = p2 + d
        p4 = p3 + d

        background(0)

        translate(140, 0)

        # Draw gray box
        stroke(153)
        line((p3, p3), (p2, p3))
        line((p2, p3), (p2, p2))
        line((p2, p2), (p3, p2))
        line((p3, p2), (p3, p3))

        # Draw white points
        stroke(255)
        point(p1, p1)
        point(p1, p3)
        point(p2, p4)
        point(p3, p1)
        point(p4, p2)
        point(p4, p4)

if __name__ == '__main__':
        print("Translate not yet implemented")
        # run(renderer='skia')
