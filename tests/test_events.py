from p5 import *

def setup():
    size(400, 400)
    background(1, 1, 1, 1)
    no_stroke()

def draw():
    background(1, 1, 1, 1)
    if mouse_is_pressed:
        if mouse_button == MOUSE_LEFT:
            fill(0.9, 0.1, 0.1, 1)
        elif mouse_button == MOUSE_RIGHT:
            fill(0.1, 0.9, 0.1, 1)
        elif mouse_button == MOUSE_CENTER:
            fill(0.1, 0.1, 0.9, 1)
        else:
            fill(0.5, 0.5, 0.5, 1)
    else:
        fill(0.1, 0.1, 0.1, 1)
    if mouse_is_dragging:
        square((mouse_x, mouse_y), 10, mode='RADIUS')
    else:
        circle((mouse_x, mouse_y), 10, mode='CENTER')

def mouse_clicked(e): print(e)
def mouse_dragged(e): print(e)
def mouse_moved(e): print(e)
def mouse_pressed(e): print(e)
def mouse_released(e): print(e)
def mouse_wheel(e): print(e)

def key_pressed(e): print(e)
def key_released(e): print(e)
def key_typed(e): print(e)

run()
