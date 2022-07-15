from p5 import *

def setup():
    size(640, 640)

def draw():
    background(220)
    stroke_weight(20)
    point(20, 30)
    beginShape(POINTS)
    vertex(30, 20)
    vertex(85, 20)
    vertex(85, 75)
    vertex(30, 75)
    endShape()

def mouse_pressed():
    redraw()


run(renderer='skia')