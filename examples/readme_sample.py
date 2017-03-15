from p5py import *

def setup():
    background(255, 255, 255)

    fill(153)
    rect(5, 5, 30, 30)

    fill(204, 102, 0)
    rect(5, 45, 30, 30)

    fill(204, 204, 204)
    stroke(204, 102, 0)
    rect(5, 85, 30, 30)

    no_fill()
    rect(5, 125, 30, 30)

    fill(204, 204, 204)
    no_stroke()
    rect(5, 165, 30, 30)

    stroke(51, 51, 51)
    for i, w in enumerate([1, 2, 5, 10, 20]):
        stroke_weight(w)
        line((45, 5 + i*40), (75, 35 + i*40))
        point(100, 20 + i*40)

    stroke_weight(1)
    ellipse(140, 20, 30, 30)
    ellipse(180, 20, 15, 30)
    ellipse(160, 60, 60, 30)

    triangle((160, 85), (125, 125), (195, 155))
    quad((125, 130), (195, 160), (195, 195), (125, 195))
