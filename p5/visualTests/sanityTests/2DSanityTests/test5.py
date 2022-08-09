from p5 import *

def setup():
    size(640, 360)

def draw():
    background(255)
    text("p5py", mouse_x, mouse_y)
    stroke(0)
    text_size(20)
    fill(220, 180, 200)
    stroke_weight(1)
    text("p5py", mouse_x + 50, mouse_y + 50)
    no_fill()
    text("p5py", mouse_x + 100, mouse_y + 100)
    no_stroke()
    fill(47, 213, 28)
    text("p5py", mouse_x + 150, mouse_y + 150)
    stroke(47, 213, 28)
    text("p5py", mouse_x + 200, mouse_y + 200)
    text_size(40)
    stroke_weight(5)
    text("p5py", mouse_x + 300, mouse_y + 300)

