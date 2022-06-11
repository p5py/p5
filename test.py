from p5 import *
import skia


def setup():
    print("SETUP")
    p5.sketch.canvas.clear(skia.ColorWHITE)
    size(1000, 700)
    p5.renderer.render_rectangle(200, 300, 50, 50)
    print("frame count", frame_count)


def draw():
    if frame_count == 1:
        no_loop()
    p5.renderer.render_circle(20,20, 30)
    p5.renderer.render_circle(p5.sketch.mouseX, p5.sketch.mouseY, 30)
    print("frame count", frame_count)


if __name__ == '__main__':
    run(renderer='skia',  frame_rate=60)
