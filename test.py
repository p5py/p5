from p5 import *
import skia


def setup():
    print("SETUP")
    p5.sketch.canvas.clear(skia.ColorWHITE)
    size(1000, 700)
    p5.renderer.render_rectangle(200, 300, 50, 50)
    print("frame count", frame_count)
    no_loop()

def draw():
    p5.renderer.render_circle(20,20, 30)
    p5.renderer.render_circle(mouse_x, mouse_y, 30)
    print("frame count", frame_count)


if __name__ == '__main__':
    run(renderer='skia',  frame_rate=60)
