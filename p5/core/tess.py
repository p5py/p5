from OpenGL.GLU import (
    gluNewTess,
    gluTessCallback,
    GLU_TESS_VERTEX,
    GLU_TESS_BEGIN,
    GLU_TESS_END,
    GLU_TESS_ERROR,
    gluErrorString,
    GLU_TESS_COMBINE,
)
from OpenGL.GL import GL_TRIANGLE_FAN, GL_TRIANGLE_STRIP, GL_TRIANGLES, GL_LINE_LOOP
import numpy as np


class Tessellator:
    def __init__(self):
        self.tess = gluNewTess()
        self.primitives = []  # [[gl_type, vertices, idx]...]
        self.vertices = []  # Vertices for the current shape
        self.type = None  # Type for the current shape

        gl_mode_map = {
            GL_TRIANGLE_FAN: "triangle_fan",
            GL_TRIANGLE_STRIP: "triangle_strip",
            GL_TRIANGLES: "triangles",
            GL_LINE_LOOP: "line_loop",
        }

        def end_shape_handler():
            curr_obj = [
                gl_mode_map[self.type],
                self.vertices,
                np.arange(len(self.vertices), dtype=np.uint32),
            ]
            self.primitives.append(curr_obj)

        def begin_shape_handler(x):
            self.type = x
            self.vertices = []

        def vertex_handler(v):
            self.vertices.append(v)

        def combine_handler(new_vert, _, __):
            return new_vert

        # Register Callbacks
        gluTessCallback(self.tess, GLU_TESS_VERTEX, vertex_handler)
        gluTessCallback(self.tess, GLU_TESS_END, end_shape_handler)
        gluTessCallback(
            self.tess, GLU_TESS_ERROR, lambda x: print("Error", gluErrorString(x))
        )
        gluTessCallback(self.tess, GLU_TESS_BEGIN, begin_shape_handler)
        gluTessCallback(self.tess, GLU_TESS_COMBINE, combine_handler)

    def get_result(self):
        """Returns the current primitive_list and clears it
        For the format of the draw queue, see the definition of self.primitive_list in `__init__`
        """
        res = self.primitives
        self.primitives = []
        return res
