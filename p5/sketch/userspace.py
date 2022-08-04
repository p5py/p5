#
# part of p5: a python package based on processing
# copyright (c) 2017-2019 abhik pal
#
# this program is free software: you can redistribute it and/or modify
# it under the terms of the gnu general public license as published by
# the free software foundation, either version 3 of the license, or
# (at your option) any later version.
#
# this program is distributed in the hope that it will be useful, but
# without any warranty; without even the implied warranty of
# merchantability or fitness for a particular purpose. see the gnu
# general public license for more details.
#
# you should have received a copy of the gnu general public license
# along with this program. if not, see <http://www.gnu.org/licenses/>.
#
"""Userspace functions"""

import __main__

import math
import numpy as np
import builtins
import sys
import time
from functools import wraps

from .events import handler_names

from ..core import p5
from ..pmath import matrix

__all__ = [
    "no_loop",
    "loop",
    "redraw",
    "size",
    "title",
    "no_cursor",
    "cursor",
    "exit",
    "draw",
    "setup",
    "run",
    "save_frame",
    "save",
    "is_looping",
    "set_frame_rate",
]

builtins.width = 360
builtins.height = 360
builtins.pixel_x_density = 1
builtins.pixel_y_density = 1

builtins.title = "p5"
builtins.frame_count = -1
builtins.frame_rate = None
# TODO: Implement focussed for Vispy, only implemented in Skia2DRenderer
builtins.focused = True

builtins.mouse_button = None
builtins.mouse_is_pressed = False
builtins.mouse_x = 0
builtins.mouse_y = 0
builtins.pmouse_x = 0
builtins.pmouse_y = 0
# TODO: Add docs for moved_x and moved_y
builtins.moved_x = 0
builtins.moved_y = 0

builtins.key = None
builtins.key_is_pressed = False

builtins.pixels = None
builtins.start_time = 0
builtins.current_renderer = None


def _fix_interface(func):
    """Make sure that `func` takes at least one argument as input.

    :returns: a new function that accepts arguments.
    :rtype: func
    """

    @wraps(func)
    def fixed_func(*args, **kwargs):
        return_value = func()
        return return_value

    if func.__code__.co_argcount == 0:
        return fixed_func
    else:
        return func


def draw():
    """Continuously execute code defined inside.

    The `draw()` function is called directly after `setup()` and all
    code inside is continuously executed until the program is stopped
    (using `exit()`) or `no_loop()` is called.

    """
    pass


def setup():
    """Called to setup initial sketch options.

    The `setup()` function is run once when the program starts and is
    used to define initial environment options for the sketch.

    """
    pass


def run(
    sketch_setup=None, sketch_draw=None, frame_rate=60, mode="P2D", renderer="vispy"
):
    """Run a sketch.

    if no `sketch_setup` and `sketch_draw` are specified, p5 automatically
    "finds" the user-defined setup and draw functions.

    :param sketch_setup: The setup function of the sketch (None by
         default.)
    :type sketch_setup: function

    :param sketch_draw: The draw function of the sketch (None by
        default.)
    :type sketch_draw: function

    :param frame_rate: The target frame rate for the sketch.
    :type frame_rate: int :math:`\geq 1`

    """
    # get the user-defined setup(), draw(), and handler functions.
    if sketch_setup is not None:
        setup_method = sketch_setup
    elif hasattr(__main__, "setup"):
        setup_method = __main__.setup
    else:
        setup_method = setup

    if sketch_draw is not None:
        draw_method = sketch_draw
    elif hasattr(__main__, "draw"):
        draw_method = __main__.draw
    else:
        draw_method = draw

    handlers = dict()
    for handler in handler_names:
        if hasattr(__main__, handler):
            hfunc = getattr(__main__, handler)
            handlers[handler] = _fix_interface(hfunc)

    if renderer == "vispy":
        import vispy

        vispy.use("glfw")
        from p5.sketch.Vispy2DRenderer.base import VispySketch
        from vispy import app

        builtins.current_renderer = "vispy"

        if mode == "P2D":
            p5.mode = "P2D"
            from p5.sketch.Vispy2DRenderer.renderer2d import VispyRenderer2D

            p5.renderer = VispyRenderer2D()
        elif mode == "P3D":
            p5.mode = "P3D"
            from p5.sketch.Vispy3DRenderer.renderer3d import Renderer3D

            p5.renderer = Renderer3D()
        else:
            ValueError("Invalid Mode %s" % mode)

        p5.sketch = VispySketch(setup_method, draw_method, handlers, frame_rate)
        physical_width, physical_height = p5.sketch.physical_size
        width, height = p5.sketch.size

        builtins.pixel_x_density = physical_width // width
        builtins.pixel_y_density = physical_height // height
        builtins.start_time = time.perf_counter()

        p5.sketch.timer.start()

        app.run()
        exit()
    elif renderer == "skia":
        from p5.sketch.Skia2DRenderer.base import SkiaSketch
        from p5.sketch.Skia2DRenderer.renderer2d import SkiaRenderer

        builtins.current_renderer = renderer
        if mode == "P2D":
            p5.mode = "P2D"
            p5.renderer = SkiaRenderer()
        elif mode == "P3D":
            raise NotImplementedError("3D mode is not available in skia")
        p5.sketch = SkiaSketch(setup_method, draw_method, handlers, frame_rate)
        p5.sketch.start()
    else:
        raise NotImplementedError("Invalid Renderer %s" % renderer)


def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    builtins.title = new_title
    p5.sketch.title = new_title


def size(width, height):
    """Resize the sketch window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.width = int(width)
    builtins.height = int(height)
    p5.sketch.size = (builtins.width, builtins.height)

    # update the look at matrix coordinates according to sketch size
    if p5.mode == "P3D":
        eye = np.array((0, 0, height / math.tan(math.pi / 6)))
        p5.renderer.lookat_matrix = matrix.look_at(
            eye, np.array((0, 0, 0)), np.array((0, 1, 0))
        )
        p5.renderer.camera_pos = eye


def no_loop():
    """Stop draw() from being continuously called.

    By default, the sketch continuously calls `draw()` as long as it
    runs. Calling `no_loop()` stops draw() from being called the next
    time. Note that this only prevents execution of the code inside
    `draw()` and the user can manipulate the screen contents through
    event handlers like `mouse_pressed()`, etc.

    """
    p5.sketch.looping = False
    p5.sketch.redraw = True


def loop():
    """Make sure `draw()` is being called continuously.

    `loop()` reverts the effects of `no_loop()` and allows `draw()` to
    be called continously again.

    """
    p5.sketch.looping = True


def redraw():
    """Call `draw()` once.

    If looping has been disabled using `no_loop()`, `redraw()` will
    make sure that `draw()` is called *exactly* once.

    """
    if not p5.sketch.looping:
        p5.sketch.redraw = True


def exit():
    """Exit the sketch.

    `exit()` makes sure that necessary cleanup steps are performed
    before exiting the sketch.

    """
    if not (p5.sketch is None):
        if builtins.current_renderer == "vispy":
            p5.sketch.exit()


def no_cursor():
    """Hide the mouse cursor."""
    # window.set_mouse_visible(False)
    raise NotImplementedError


def cursor(cursor_type="ARROW"):
    """Set the cursor to the specified type.

    :param cursor_type: The cursor type to be used (defaults to
        'ARROW'). Should be one of: {'ARROW','CROSS','HAND', 'MOVE',
        'TEXT', 'WAIT'}
    :type cursor_type: str

    """
    # cursor_map = {
    #     'ARROW': window.CURSOR_DEFAULT,
    #     'CROSS': window.CURSOR_CROSSHAIR,
    #     'HAND': window.CURSOR_HAND,
    #     'MOVE': window.CURSOR_SIZE,
    #     'TEXT': window.CURSOR_TEXT,
    #     'WAIT': window.CURSOR_WAIT
    # }
    # selected_cursor = cursor_map.get(cursor_type, 'ARROW')
    # cursor = window.get_system_mouse_cursor(selected_cursor)
    # window.set_mouse_visible(True)
    # window.set_mouse_cursor(cursor)
    raise NotImplementedError


def save(filename="screen.png"):
    """Save an image from the display window.

    Saves an image from the display window. Append a file extension to
    the name of the file, to indicate the file format to be used.If no
    extension is included in the filename, the image will save in PNG
    format and .png will be added to the name. By default, these files
    are saved to the folder where the sketch is saved. Alternatively,
    the files can be saved to any location on the computer by using an
    absolute path (something that starts with / on Unix and Linux, or
    a drive letter on Windows).

    :param filename: Filename of the image (defaults to
        ``screen.png``)

    :type filename: str

    """
    # TODO: images saved using ``save()`` should *not* be numbered.
    # --abhikpal (2018-08-14)
    p5.sketch.screenshot(filename)


def save_frame(filename="screen.png"):
    """Save a numbered sequence of images whenever the function is run.

    Saves a numbered sequence of images, one image each time the
    function is run. To save an image that is identical to the display
    window, run the function at the end of :meth:`p5.draw` or within
    mouse and key events such as :meth:`p5.mouse_pressed` and
    :meth:`p5.key_pressed`.

    If save_frame() is used without parameters, it will save files as
    screen-0000.png, screen-0001.png, and so on. Append a file
    extension, to indicate the file format to be used. Image files are
    saved to the sketch's folder. Alternatively, the files can be
    saved to any location on the computer by using an absolute path
    (something that starts with / on Unix and Linux, or a drive letter
    on Windows).

    :param filename: name (or name with path) of the image file.
        (defaults to ``screen.png``)

    :type filename: str

    """
    # todo: allow setting the frame number in the file name of the
    # saved image (instead of using the default sequencing) --abhikpal
    # (2018-08-14)
    p5.sketch.queue_screenshot(filename)


# TODO: Add support to calculate the current frame_rate
# TODO: Deprecate set_frame_rate and use frame_rate(), current frame_rate should return as per p5.js API
def set_frame_rate(fps):
    """Sets the frame_rate for the current sketch

    Args:
        fps (int): Number of frames to be displayed per second

    """
    if builtins.current_renderer != "skia":
        raise NotImplementedError("set_frame_rate is only supported in skia")

    p5.sketch.frame_rate = fps


def is_looping():
    """Returns the current looping state of the sketch"""
    return p5.sketch.looping
