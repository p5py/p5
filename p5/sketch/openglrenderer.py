from abc import ABC
import numpy as np

# Abstract class that contains common code for OpenGL renderers
class OpenGLRenderer(ABC):
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
