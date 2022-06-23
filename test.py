from this import d
from p5 import *
import skia

def setup():
    print("SETUP")
    p5.sketch.canvas.clear(skia.ColorWHITE)
    size(1000, 700)
    p5.renderer.render_rectangle(200, 300, 50, 50)
    # print("frame count", frame_count)
    no_loop()

def draw():
    p5.renderer.render_circle(20,20, 80)
    # print(mouse_x, mouse_y, moved_x, moved_y)
    # p5.renderer.render_circle(mouse_x, mouse_y, abs(moved_x) + abs(moved_y))
    p5.renderer.render_circle(mouse_x, mouse_y, 30)
    # print("frame count", frame_count)
    print(key_is_pressed, key)
    
def mouse_pressed(event):
    if mouse_button == 'LEFT':
        redraw()
    elif mouse_button == 'RIGHT':
        loop()
    elif mouse_button == 'MIDDLE':
        print(is_looping())
        print("middle button is pressed")

# def mouse_released(event):
#     print("event", event.button)
    
# def mouse_clicked(event):
#     print("event", event.button)

# def mouse_double_clicked(event):
#     print(event, event.button, "dclicks")
    
# def mouse_wheel(event):
#     print(event.scroll)

def key_release(event):
    print(event.key)

def key_pressed(event):
    print(event.key)

def key_typed(event):
    print("typed", event.key)

if __name__ == '__main__':
    run(renderer='skia',  frame_rate=10)
