from p5 import *

def setup():
        # Sets the screen to be 720 pixels wide and 400 pixels high
        size(720, 400)

def draw():
        background(0)
        no_stroke()

        fill(204)
        triangle((18, 18), (18, 360), (81, 360))

        fill(102)
        rect((81, 81), 63, 63)

        fill(204)
        quad((189, 18), (216, 18), (216, 360), (144, 360))

        fill(255)
        ellipse((252, 144), 72, 72)

        fill(204)
        triangle((288, 18), (351, 360), (288, 360))

        fill(255)
        arc((479, 300), 280, 280, PI, TWO_PI)

if __name__ == '__main__':
        run()
