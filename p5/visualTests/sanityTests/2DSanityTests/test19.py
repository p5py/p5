from p5 import *

coswave = []

def setup():
        size(720, 360)
        for i in range(width):
                amount = remap(i, [0, width], [0, PI])
                coswave.append(abs(cos(amount)))

        background(255)
        no_loop()

def draw():
        y1 = 0
        y2 = height/3
        for i in range(0, width, 3):
                stroke(coswave[i] * 255)
                line((i, y1), (i, y2))

        y1 = y2
        y2 = y1 + y1
        for i in range(0, width, 3):
                stroke(coswave[i]*255 / 4)
                (line((i, y1), (i, y2)))

        y1 = y2
        y2 = height
        for i in range(0, width, 3):
                stroke(255 - coswave[i] * 255)
                line((i, y1), (i, y2))

if __name__ == '__main__':
  run()