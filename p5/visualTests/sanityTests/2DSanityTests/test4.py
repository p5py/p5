from p5 import *


def setup():
    size(640, 360)


def draw():
    if frame_count > 30:
        exit()
    # Sets the screen to be 640 pixels wide and 360 pixels high

    # Set the background to black and turn off the fill color
    background(0)
    no_fill()

    # The two parameters of the point() method each specify coordinates.
    # The first parameter is the x-coordinate and the second is the Y
    stroke(255)
    point(width * 0.5, height * 0.1)
    point(width * 0.5, height * 0.9)
    # Coordinates are used for drawing all shapes, not just points.
    # Parameters for different functions are used for different purposes.
    # For example, the first parameter to line() specify
    # the coordinates of the first endpoint and the second parameter
    # specify the second endpoint
    stroke(0, 153, 255)
    line((0, height * 0.33), (width, height * 0.33))

    # By default, the first parameter to rect() is the
    # coordinates of the upper-left corner and the second and third
    # parameter is the width and height
    stroke(255, 153, 0)
    rect(width * 0.25, height * 0.1, width * 0.5, height * 0.8)
