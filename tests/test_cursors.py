from p5 import *

def setup():
    size(200, 200)
    background(1, 1, 1, 1)

def draw():
    background(1, 1, 1, 1)

def key_pressed(event):
    if event.key == 'A':
        cursor('ARROW')
    elif event.key == 'C':
        cursor('CROSS')
    elif event.key == 'H':
        cursor('HAND')
    elif event.key == 'M':
        cursor('MOVE')
    elif event.key == 'T':
        cursor('TEXT')
    elif event.key == 'W':
        cursor('WAIT')
    else:
        no_cursor()

run()
    
