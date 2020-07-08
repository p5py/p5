from abc import ABC
import numpy as np


# Abstract class that contains common code for OpenGL renderers
class OpenGLRenderer(ABC):
    def __init__(self):
        self.default_prog = None
        self.fbuffer_prog = None

        self.fbuffer = None
        self.fbuffer_tex_front = None
        self.fbuffer_tex_back = None

        self.vertex_buffer = None
        self.index_buffer = None

        # Renderer Globals: USEFUL CONSTANTS
        self.COLOR_WHITE = (1, 1, 1, 1)
        self.COLOR_BLACK = (0, 0, 0, 1)
        self.COLOR_DEFAULT_BG = (0.8, 0.8, 0.8, 1.0)

        # Renderer Globals: STYLE/MATERIAL PROPERTIES
        #
        self.background_color = self.COLOR_DEFAULT_BG

        self.fill_color = self.COLOR_WHITE
        self.fill_enabled = True

        self.stroke_color = self.COLOR_BLACK
        self.stroke_enabled = True

        self.tint_color = self.COLOR_BLACK
        self.tint_enabled = False

        # Renderer Globals: Curves
        self.stroke_weight = 1
        self.stroke_cap = 2
        self.stroke_join = 0

        # Renderer Globals
        # VIEW MATRICES, ETC
        #
        self.viewport = None
        self.texture_viewport = None
        self.transform_matrix = np.identity(4)
        self.projection_matrix = np.identity(4)

        # Renderer Globals: RENDERING
        self.draw_queue = []

    def render_default(self, draw_type, draw_queue):
        # 1. Get the maximum number of vertices persent in the shapes
        # in the draw queue.
        #
        if len(draw_queue) == 0:
            return

        num_vertices = 0
        for vertices, _, _ in draw_queue:
            num_vertices = num_vertices + len(vertices)

        # 2. Create empty buffers based on the number of vertices.
        #
        data = np.zeros(num_vertices,
                        dtype=[('position', np.float32, 3),
                               ('color', np.float32, 4)])

        # 3. Loop through all the shapes in the geometry queue adding
        # it's information to the buffer.
        #
        sidx = 0
        draw_indices = []
        for vertices, idx, color in draw_queue:
            num_shape_verts = len(vertices)

            data['position'][sidx:(sidx + num_shape_verts), ] = np.array(vertices)

            color_array = np.array([color] * num_shape_verts)
            data['color'][sidx:sidx + num_shape_verts, :] = color_array

            draw_indices.append(sidx + idx)

            sidx += num_shape_verts

        self.vertex_buffer.set_data(data)
        self.index_buffer.set_data(np.hstack(draw_indices))

        # 4. Bind the buffer to the shader.
        #
        self.default_prog.bind(self.vertex_buffer)

        # 5. Draw the shape using the proper shape type and get rid of
        # the buffers.
        #
        self.default_prog.draw(draw_type, indices=self.index_buffer)

    def cleanup(self):
        """Run the clean-up routine for the renderer.

        This method is called when all drawing has been completed and the
        program is about to exit.

        """
        self.default_prog.delete()
        self.fbuffer_prog.delete()
        self.fbuffer.delete()

    def _transform_vertices(self, vertices, local_matrix, global_matrix):
        return np.dot(np.dot(vertices, local_matrix.T), global_matrix.T)[:, :3]
