from p5 import *

mx = 0
my = 0
easing = 0.05
radius = 24
edge = 100
inner = edge + radius

def setup():
        size(640, 360)
        no_stroke()
        ellipse_mode("RADIUS")
        rect_mode("CORNER")

def draw():
        background(51)

        global mx, my, easing, radius, edge, inner

        if abs(mouse_x - mx) > 0.1:
                mx = mx + (mouse_x - mx) * easing
        if abs(mouse_y - my) > 0.1:
                my = my + (mouse_y- my) * easing

        mx = constrain(mx, inner, width - inner)
        my = constrain(my, inner, height - inner)
        fill(76)
        rect(edge, edge, width - 2*edge, height - 2*edge)
        fill(255)
        ellipse([mx, my], radius, radius)

if __name__ == '__main__':
        run(renderer='skia')
