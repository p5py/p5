from p5 import *

rectWidth = 0

def setup():
        global rectWidth

        size(640, 360)
        no_stroke()
        background(0)

        rectWidth = width/4

def draw():
        pass

def key_pressed():
        global rectWidth
        keyIndex = -1

        if ord(str(key)) >= ord(str("A")) and ord(str(key)) <= ord(str("Z")):
                keyIndex = ord(str(key)) - ord(str("A"))
        elif ord(str(key)) >= ord(str("a")) and ord(str(key)) <= ord(str("z")):
                keyIndex = ord(str(key)) - ord(str("a"))

        if keyIndex == -1:
                # If it's not a letter key, clear the screen
                background(0)
        else:
                # It's a letter key, fill a rectangle
                fill(millis()%255)
                x = remap(keyIndex, [0, 25], [0, width - rectWidth])
                rect((x, 0), rectWidth, height)

if __name__ == '__main__':
        run()