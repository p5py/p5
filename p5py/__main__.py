import sys
import os

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from . import globs
from . import _attribs as attr

if __name__ == '__main__':
    sketch_file = sys.argv[-1]
    sketch_name = sketch_file.rsplit('.', 1)[0].rsplit('/', 1)[-1]

    sys.path.insert(0, os.path.dirname(sketch_file))
    
    pygame.init()
    pygame.display.set_mode([globs.WIDTH, globs.HEIGHT], DOUBLEBUF|OPENGL)
    pygame.display.set_caption(sketch_name.split('.')[-1])
    
    glClearColor(*attr.color_background)
    glColor4f(*attr.color_fill)
    gluOrtho2D(0, 1, -1, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    glEnable (GL_BLEND)
    glBlendFunc (GL_ONE, GL_ONE)

    sketch = __import__(sketch_name)

    if 'setup' in dir(sketch):
        sketch.setup()
        pygame.time.wait(10)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        if 'draw' in dir(sketch):
            sketch.draw()
        # glClear(GL_COLOR_BUFFER_BIT)

        pygame.display.flip()
        pygame.time.wait(10)
