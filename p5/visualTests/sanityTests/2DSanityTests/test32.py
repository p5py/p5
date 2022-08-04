from p5 import *

maxHeight = 40
minHeight = 20
letterHeight = maxHeight  # Height of the letters
letterWidth = 20  # Width of the letter

x = -letterWidth  # X position of the letters
y = 0  # Y position of the letters

newletter = False
numChars = 26  # There are 26 characters in the alphabet
colors = []


def setup():
    global colors

    size(640, 360)
    no_stroke()
    color_mode("HSB", numChars)
    background(numChars / 2)

    background(0)
    # Set a hue value for each key
    for i in range(numChars):
        colors.append(Color(i, numChars, numChars))


def draw():
    global newletter
    if newletter == True:
        # Draw the "letter"
        y_pos = 0
        if letterHeight == maxHeight:
            y_pos = y
            rect((x, y_pos), letterWidth, letterHeight)
        else:
            y_pos = y + minHeight
            rect((x, y_pos), letterWidth, letterHeight)
            fill(numChars / 2)
            rect((x, y_pos - minHeight), letterWidth, letterHeight)

        newletter = False


def key_pressed():
    global letterHeight, newletter, x, y
    #  If the key is between 'A'(65) to 'Z' and 'a' to 'z'(122)
    if (
        ord(str(key)) >= ord(str("A"))
        and ord(str(key)) <= ord(str("Z"))
        or ord(str(key)) >= ord(str("a"))
        and ord(str(key)) <= ord(str("z"))
    ):
        keyIndex = 0
        if ord(str(key)) <= ord(str("Z")):
            keyIndex = ord(str(key)) - ord(str("A"))
            letterHeight = maxHeight
            fill(colors[keyIndex])
        else:
            keyIndex = ord(str(key)) - ord(str("a"))
            letterHeight = minHeight
            fill(colors[keyIndex])
    else:
        fill(0)
        letterHeight = 10

    newletter = True
    # Update the "letter" position
    x = x + letterWidth

    # Wrap horizontally
    if x > width - letterWidth:
        x = 0
        y = y + maxHeight

    # Wrap vertically
    if y > height - letterHeight:
        y = 0  # reset y to 0
