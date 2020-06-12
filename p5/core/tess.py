from OpenGL.GLU import gluNewTess, gluTessCallback, GLU_TESS_VERTEX, GLU_TESS_BEGIN, GLU_TESS_END, GLU_TESS_ERROR, gluErrorString
from OpenGL.GL import GL_TRIANGLE_FAN, GL_TRIANGLE_STRIP, GL_TRIANGLES, GL_LINE_LOOP

class Tessellator:
    def __init__(self):
        self.tess = gluNewTess()
        self.draw_queue = [] # [[shape_type, v1, v2, ...], [shape_type, v1, v2, ...), ...]

        def to_tess_string(x):
            if x == GL_TRIANGLE_FAN:
                return "GL_TRIANGLE_FAN"
            elif x == GL_LINE_LOOP:
                return "GL_LINE_LOOP"
            elif x == GL_TRIANGLE_STRIP:
                return "GL_TRIANGLE_STRIP"
            elif x == GL_TRIANGLES:
                return "GL_TRIANGLES"

        def end_shape_handler():
            print("End")

        def begin_shape_handler(x):
            print("Begin", to_tess_string(x))
            self.draw_queue.append([x])

        def vertex_handler(v):
            print("Vertex", v)
            self.draw_queue[-1].append(v)

        # Register Callbacks
        gluTessCallback(self.tess, GLU_TESS_VERTEX, vertex_handler)
        gluTessCallback(self.tess, GLU_TESS_END, end_shape_handler)
        gluTessCallback(self.tess, GLU_TESS_ERROR, lambda x: print("Error", gluErrorString(x)))
        gluTessCallback(self.tess, GLU_TESS_BEGIN, begin_shape_handler)

    # Returns the current draw_queue and clears it
    def process_draw_queue(self):
        res = self.draw_queue
        self.draw_queue = []
        return res
