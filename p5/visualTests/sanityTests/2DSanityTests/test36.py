from p5 import *

angles = [30, 10, 45, 35, 60, 38, 75, 67]


def setup():
    # Sets the screen to be 720 pixels wide and 400 pixels high
    size(720, 400)
    no_loop()
    no_stroke()


def draw():
    background(100)
    pie_chart(300, angles)


def pie_chart(diameter, data):
    lastAngle = 0
    for i in range(len(data)):
        gray = remap(i, [0, len(data)], [0, 255])
        fill(gray)
        arc(
            (width / 2, height / 2),
            diameter,
            diameter,
            lastAngle,
            lastAngle + radians(angles[i])
        )

        lastAngle += radians(angles[i])
