from p5 import *

unit = 40
count = None
mods = []


def setup():
    size(640, 360)
    no_stroke()

    global count, unit, mods
    wideCount = width / unit
    highCount = height / unit

    count = wideCount * highCount
    index = 0
    for y in range(int(highCount)):
        for x in range(int(wideCount)):
            mods.append(
                Module(
                    x * unit,
                    y * unit,
                    unit / 2,
                    unit / 2,
                    random_uniform(0.05, 0.8),
                    unit,
                )
            )


def draw():
    background(0)
    for mod in mods:
        mod.update()
        mod.display()


class Module:
    def __init__(self, xOffsetTemp, yOffsetTemp, xTemp, yTemp, speedTemp, tempUnit):
        self.xOffset = xOffsetTemp
        self.yOffset = yOffsetTemp

        self.x = xTemp
        self.y = yTemp
        self.speed = speedTemp
        self.unit = tempUnit

        self.xDirection = 1
        self.yDirection = 1

    def update(self):
        self.x = self.x + (self.speed * self.xDirection)
        if self.x > unit or self.x <= 0:
            self.xDirection *= -1
            self.x += self.xDirection
            self.y += self.yDirection
        elif self.y > unit or self.y <= 0:
            self.yDirection *= -1
            self.y += yDirection

    def display(self):
        fill(255)
        ellipse((self.xOffset + self.x, self.yOffset + self.y), 6, 6)
