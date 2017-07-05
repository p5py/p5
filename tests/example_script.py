from p5 import *

background_color = (0.1, 0.1, 0.1, 1.0)

def setup():
    size(800, 600)
    title("Example Sketch")
    #no_stroke()

def draw():
    scale(2.0)
    background(*background_color)

    with push_matrix():
        translate(160, 150)

        fill(1.0, 0.6, 0.0, 1.0)
        square((-30, -30), 60)
        square((-30, -50), 20)

        fill(*background_color)
        square((-10, -10), 20)

    with push_matrix():
        translate(240, 170)

        fill(1.0, 0.8, 0.0, 1.0)
        rect((-30, -50), 60, 100)

        fill(*background_color)
        rect((-30, -30), 40, 20)
        rect((-10, 10), 40, 20)

if __name__ == '__main__':
    run()
