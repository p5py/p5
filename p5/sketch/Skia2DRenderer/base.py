from p5.core import p5

import skia
from OpenGL import GL

import copy
from ..events import handler_names
from .handlers import *
from .util import *


def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing."""
    pass


class SkiaSketch:
    def __init__(self, setup_method, draw_method, handlers=dict(), frame_rate=60):
        self._size = (600, 400)
        self.setup_method = setup_method
        self.draw_method = draw_method

        self.surface = None
        self.context = None
        self.window = None
        self.canvas = None

        self.main_loop_state = True
        self.looping = True
        self.redraw = False

        self.paint = skia.Paint()
        self.paint.setAntiAlias(True)
        self.path = skia.Path()

        self.frame_rate = frame_rate
        self.pixel_density = 1

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

        self.handlers = {}

        for handler_name in handler_names:
            self.handlers[handler_name] = handlers.get(handler_name, _dummy)

        self.handler_queue = []

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
            raise RuntimeError("glfw.init() failed")

        window = glfw.create_window(*self._size, "p5py", None, None)
        glfw.make_context_current(window)
        return window

    def skia_surface(self):
        self.context = skia.GrDirectContext.MakeGL()
        width, height = glfw.get_framebuffer_size(self.window)
        backend_render_target = skia.GrBackendRenderTarget(
            width,
            height,
            0,  # sampleCnt
            0,  # stencilBits
            skia.GrGLFramebufferInfo(0, GL.GL_RGBA8),
        )
        surface = skia.Surface.MakeFromBackendRenderTarget(
            self.context,
            backend_render_target,
            skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType,
            skia.ColorSpace.MakeSRGB(),
        )
        assert surface is not None
        return surface

    # create a new surface everytime
    def create_surface(self):
        self._size = glfw.get_framebuffer_size(self.window)
        builtins.width, builtins.height = self._size
        self.surface = self.skia_surface()
        self.canvas = self.surface.getCanvas()
        p5.renderer.initialize_renderer(self.canvas, self.paint, self.path)

    def main_loop(self):
        last_render_call_time = 0
        # Before starting the main while loop, check whether no_loop is called
        # If called we have to render a frame once
        # Set redraw and looping to False
        # This is done to ensure draw() is called atleast once

        while self.main_loop_state:
            if (
                self.resized
                and (self.looping or self.redraw)
                and (time() - last_render_call_time) > 1 / self.frame_rate
            ):
                builtins.frame_count += 1
                with self.surface as self.canvas:
                    self.draw_method()

                p5.renderer._store_surface_state()
                self.surface.flushAndSubmit()
                glfw.swap_buffers(self.window)
                p5.renderer._restore_surface_state()
                last_render_call_time = time()

                # If redraw == True, we have rendered the frame once
                # Now don't render the next one
                if self.redraw:
                    self.redraw = False

                # Reset every style values back to default
                # TODO: Find a way to reset values of Graphic objects as well,
                # TODO: we can probably emit event after each loop to notify all graphics object
                p5.renderer.reset()

            self.poll_events()
            while len(self.handler_queue) != 0:
                function, event = self.handler_queue.pop(0)
                event._update_builtins()
                function(event)

    def start(self):
        self.window = self.glfw_window()
        self.create_surface()
        self.assign_callbacks()
        p5.renderer.initialize_renderer(self.canvas, self.paint, self.path)

        # We don't draw the buffer from scratch each time, instead store the current state of surface
        # and restore it after swapping the buffer
        self.setup_method()
        p5.renderer.render()

        # Get snapshot of surface
        p5.renderer._store_surface_state()

        # Write to secondary buffer
        self.surface.flushAndSubmit()
        glfw.swap_buffers(self.window)

        p5.renderer._restore_surface_state()
        self.surface.flushAndSubmit()

        # Buffers are swapped twice so that both buffers have the same initial surface state
        glfw.swap_buffers(self.window)

        self.main_loop()
        self.clean_up()

    def resize(self):
        # when glfw changes the framebuffer size, we will be resized completely
        # until then hold the rendering calls
        self.resized = False

        # call change the window size(), this will not be done instantly
        # but after some time and a frame_buffer_changed callback will occur on
        # on a different thread
        glfw.set_window_size(self.window, *self.size)

    def poll_events(self):
        glfw.poll_events()
        if glfw.get_key(
            self.window, glfw.KEY_ESCAPE
        ) == glfw.PRESS or glfw.window_should_close(self.window):
            glfw.set_window_should_close(self.window, 1)
            self.main_loop_state = False

    # Callbacks and handlers
    def assign_callbacks(self):
        glfw.set_framebuffer_size_callback(
            self.window, self.frame_buffer_resize_callback_handler
        )

        glfw.set_key_callback(self.window, on_key_press)
        glfw.set_char_callback(self.window, on_key_char)
        glfw.set_mouse_button_callback(self.window, on_mouse_button)
        glfw.set_scroll_callback(self.window, on_mouse_scroll)
        glfw.set_cursor_pos_callback(self.window, on_mouse_motion)
        glfw.set_window_close_callback(self.window, on_close)
        glfw.set_window_focus_callback(self.window, on_window_focus)

    def frame_buffer_resize_callback_handler(self, window, width, height):
        """
        Gets called whenever frame buffer resizes
        Values of width and height may not be equal to the actual window's width and height
        in Retina Display
        """
        # Callback handler for frame buffer resize events

        self.resized = False
        builtins.pixel_x_density = width / self.size[0]
        builtins.pixel_y_density = height / self.size[1]
        self.pixel_density = width * height // (self.size[0] * self.size[1])

        # Creates an Image of current surface and a copy of current style configurations
        # For the purpose of handling setup_method() re-call
        # Ref: Issue #419
        old_style = copy.deepcopy(p5.renderer.style)

        GL.glViewport(0, 0, width, height)
        self.create_surface()
        self.setup_method()
        p5.renderer._store_surface_state()
        self.surface.flushAndSubmit()
        glfw.swap_buffers(self.window)

        p5.renderer.style = old_style

        # Tell the program, we have resized the frame buffer
        # and do not rewind/clear the path
        # Restart the rendering again
        self.resized = True

    def _enqueue_event(self, handler_name, event):
        self.handler_queue.append((self.handlers[handler_name], event))

    def exit(self):
        self.clean_up()
        exit()
