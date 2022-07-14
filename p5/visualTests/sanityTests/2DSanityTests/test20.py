from p5 import *

distances = []
maxDiantance = None
spacer = None


def setup():
    size(720, 360)

    global distances, maxDiantance, spacer
    maxDistance = dist((width / 2, height / 2), (width, height))
    for x in range(width):
        d = []
        for y in range(height):
            distance = dist((width / 2, height / 2), (x, y))
            d.append((distance / maxDistance) * 255)
        distances.append(d)

    spacer = 10
    no_loop()


def draw():
    background(0)

    for x in range(0, width, spacer):
        for y in range(0, height, spacer):
            stroke(distances[x][y])
            point(x + spacer / 2, y + spacer / 2)
