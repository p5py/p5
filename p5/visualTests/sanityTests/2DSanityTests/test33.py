from p5 import *

scale = 0

def setup():
        size(640, 360)
        no_stroke()

        global scale
        scale = width/20

def draw():
        global scale
        for i in range(int(scale)):
                color_mode("RGB", (i+1) * scale * 10)
                fill(millis()%((i+1) * scale * 10))
                rect([i*scale, 0], scale, height)


if __name__ == '__main__':
        run()