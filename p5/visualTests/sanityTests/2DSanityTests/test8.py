from p5 import *

y = 0

# The statements in the setup() function
# run once when the program begins
def setup():
    size(640, 360)  # Size should be the first statement
    stroke(255)  # Set stroke color to white
    no_loop()

    global y
    y = height * 0.5


# The statements in draw() are executed until the
# program is stopped. Each statement is executed in
# sequence and after the last line is read, the first
# line is executed again.
def draw():
    background(0)  # Set the background to black
    global y
    y = y - 1
    if y < 0:
        y = height

    line((0, y), (width, y))


def mouse_pressed():
    redraw()
