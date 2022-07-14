from p5 import *

bx = 0
by = 0
boxSize = 75
overBox = False
locked = False
xOffset = 0.0
yOffset = 0.0


def setup():
    size(640, 360)

    global bx, by
    bx = width / 2.0
    by = height / 2.0
    rect_mode("RADIUS")


def draw():
    background(0)

    global bx, by, boxSize, overBox, locked, xOffset, yOffset

    # Test if the cursor is over the box
    if (mouse_x > bx - boxSize and mouse_x < bx + boxSize and
            mouse_y > by - boxSize and mouse_y < by + boxSize):
        overBox = True

        if not locked:
            stroke(255)
            fill(153)

    else:
        stroke(153)
        fill(153)
        overBox = False

    rect([bx, by], boxSize, boxSize)


def mouse_pressed():
    global bx, by, boxSize, overBox, locked, xOffset, yOffset

    if overBox:
        locked = True
        fill(255, 255, 255)
    else:
        locked = False

    xOffset = mouse_x - bx
    yOffset = mouse_y - by


def mouse_dragged():
    global bx, by, boxSize, overBox, locked, xOffset, yOffset
    if locked:
        bx = mouse_x - xOffset
        by = mouse_y - yOffset


def mouse_released():
    global locked
    locked = False
