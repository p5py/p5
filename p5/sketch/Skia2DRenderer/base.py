import builtins
from p5.core import p5

import contextlib, glfw, skia
from OpenGL import GL
from time import time
from time import time

class SkiaSketch():
    def __init__(self, setup_method, draw_method, handlers=dict(), frame_rate=60):
        self.frame_count = 0
        self._size = (600, 400)
        self.setup_method = setup_method
        self.draw_method = draw_method
        self.surface = None
        self.context = None
        self.window = None
        self.canvas = None
        self.mouseX = 0
        self.mouseY = 0
        self.main_loop_state = True
        self.looping = True
        self.paint = skia.Paint()
        self.paint.setAntiAlias(True)
        self.path = skia.Path()
        self.frame_rate = frame_rate
        self.redraw = False

        """
        resized : (boolean) 
        When we make a call to resize the window, it does not happen instantly
        but rather glfw places the resize call on a different thread and later resizes the window 
        and its framebuffer triggering their callbacks.
        This boolean variable is used to keep track whether a resize call was made and the 
        window is yet to be resized. If so, halt the rendering process and wait for the window to
        be resized.
        This is necessary to ensure correct no_loop() behaviour.
        """
        self.resized = True

        # we can discard using builtins, by using p5.variableName
        builtins.frame_count = 0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self.resize()

    def clean_up(self):
        glfw.terminate()
        self.context.abandonContext()

    def glfw_window(self):
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        # Testing will 
        window = glfw.create_window(*self._size, 'p5py', None, None)
        glfw.make_context_current(window)
        return window

    def skia_surface(self, window, size):
        # print("surface created")
        self.context = skia.GrContext.MakeGL()
        backend_render_target = skia.GrBackendRenderTarget(
            *size,
            0,  # sampleCnt
            0,  # stencilBits
            skia.GrGLFramebufferInfo(0, GL.GL_RGBA8))
        surface = skia.Surface.MakeFromBackendRenderTarget(
            self.context, backend_render_target, skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType, skia.ColorSpace.MakeSRGB())
        assert surface is not None
        return surface

    def assign_callbacks(self):
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback_handler)
        glfw.set_framebuffer_size_callback(self.window, self.frame_buffer_resize_callback_handler)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback_handler)

    # create a new surface everytime
    def create_surface(self, size=None):
        # print("create surface")
        if not size:
            size = self._size
        self._size = size
        builtins.width, builtins.height = size
        print("SIze passed ", size)
        self.surface = self.skia_surface(self.window, size)
        self.canvas = self.surface.getCanvas()
        p5.renderer.initialize_renderer(self.canvas, self.paint, self.path)

    def poll_events(self):
        glfw.poll_events()
        if (glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS or glfw.window_should_close(self.window)):
            glfw.set_window_should_close(self.window, 1)
            self.main_loop_state = False

    def main_loop(self):
        last_render_call_time = 0

        # Before starting the main while loop, check whether no_loop is called
        # If called we have to render a frame once
        # Set redraw and looping to False
        # This is done to ensure draw() is called atleast once
        # print("looping ", self.looping)

        while (self.main_loop_state):
            if self.resized and (self.looping or self.redraw) and (time() - last_render_call_time) > 1 / self.frame_rate:
                builtins.frame_count += 1
                with self.surface as self.canvas:
                    self.draw_method()
                    # print("renderer called")
                    p5.renderer.render()
                self.surface.flushAndSubmit()
                glfw.swap_buffers(self.window)
                last_render_call_time = time()

                # If redraw == True, we have rendered the frame once
                # Now don't render the next one
                if self.redraw:
                    # self.looping = False
                    self.redraw = False
            self.poll_events()

    def start(self):
        self.window = self.glfw_window()
        self.create_surface()
        self.assign_callbacks()
        p5.renderer.initialize_renderer(self.canvas, self.paint, self.path)
        self.setup_method()
        self.poll_events()
        # print("before buffers ", glfw.get_window_size(self.window), self._size)
        p5.renderer.render(rewind=False)
        self.surface.flushAndSubmit()
        glfw.swap_buffers(self.window)
        # print("BEFORE MAIN")
        self.main_loop()
        self.clean_up()

    def resize(self):
        # call change the window size(), this will not be done instantly
        # but after some time and a frame_buffer_changed callback will occur on
        # on a different thread
        glfw.set_window_size(self.window, *self.size)

        # when glfw changes the framebuffer size, we will be resized completely
        # until then hold the rendering calls
        self.resized = False
        # print(glfw.get_framebuffer_size(self.window), self._size, glfw.get_window_size(self.window))

    def frame_buffer_resize_callback_handler(self, window, width, height):
        """
        Gets called whenever frame buffer resizes
        Values of width and height may not be equal to the actual window's width and height
        in Retina Display
        """

        # print("FRAME BUFFER CALLBACK NOW ")
        # print("frame buffer size callback ", glfw.get_window_size(self.window))

        # Callback handler for frame buffer resize events
        GL.glViewport(0, 0, width, height)
        self.create_surface(size=(width, height))
        # with self.surface as self.canvas:
        #     # redraw on the canvas/ ( new frame buffer ) after resizing
        #     # and do not rewind/clear the path
        #     p5.renderer.render(rewind=False)
        # self.surface.flushAndSubmit()
        # glfw.swap_buffers(self.window)

        # Tell the program, we have resized the frame buffer
        # Restart the rendering again
        self.resized = True

    def mouse_callback_handler(self, window, xpos, ypos):
        self.mouseX = xpos
        self.mouseY = ypos

    def mouse_button_callback_handler(self, window, button, action, mods):
        # If a mouse button is pressed
        if action == glfw.PRESS:

            # Changing the values manually, at the end we will have an event handler
            # similar to vispy
            if button == glfw.MOUSE_BUTTON_LEFT:
                self.redraw = True
            if button == glfw.MOUSE_BUTTON_RIGHT:
                self.looping = True

        # If a mouse button is released
        if action == glfw.RELEASE:
            # set environment variables
            pass
