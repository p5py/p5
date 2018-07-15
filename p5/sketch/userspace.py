#
# part of p5: a python package based on processing
# copyright (c) 2017-2018 abhik pal
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
import builtins
from functools import wraps

import vispy
from vispy import app

from .base import Sketch
from .events import handler_names
from .renderer import initialize_renderer

__all__ = ['no_loop', 'loop', 'redraw', 'size', 'title', 'no_cursor',
           'cursor', 'exit', 'draw', 'setup', 'run']

default_sketch = None

builtins.width = 360
builtins.height = 360
builtins.pixel_x_density = 1
builtins.pixel_y_density = 1

builtins.title = "p5"
builtins.frame_count = -1
builtins.frame_rate = None
builtins.focused = True

builtins.mouse_button = None
builtins.mouse_is_pressed = False
builtins.mouse_is_dragging = False
builtins.mouse_x = 0
builtins.mouse_y = 0
builtins.pmouse_x = 0
builtins.pmouse_y = 0
builtins.key = None
builtins.key_is_pressed = False

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

def run(sketch_setup=None, sketch_draw=None, frame_rate=60):
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
    global default_sketch

    # get the user-defined setup(), draw(), and handler functions.
    if sketch_setup is not None:
        setup_method = sketch_setup
    elif hasattr(__main__, 'setup'):
        setup_method = __main__.setup
    else:
        setup_method = setup

    if sketch_draw is not None:
        draw_method = sketch_draw
    elif hasattr(__main__, 'draw'):
        draw_method = __main__.draw
    else:
        draw_method = draw

    handlers = dict()
    for handler in handler_names:
        if hasattr(__main__, handler):
            hfunc = getattr(__main__, handler)
            handlers[handler] = _fix_interface(hfunc)

    default_sketch = Sketch(setup_method, draw_method, handlers, frame_rate)

    physical_width, physical_height = default_sketch.physical_size
    width, height = default_sketch.size

    builtins.pixel_x_density = physical_width // width
    builtins.pixel_y_density = physical_height // height

    default_sketch.timer.start()

    app.run()
    exit()

def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    builtins.title = new_title
    default_sketch.title = new_title

def size(width, height):
    """Resize the sketch window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.width = int(width)
    builtins.height = int(height)
    default_sketch.size = (builtins.width, builtins.height)

def no_loop():
    """Stop draw() from being continuously called.

    By default, the sketch continuously calls `draw()` as long as it
    runs. Calling `no_loop()` stops draw() from being called the next
    time. Note that this only prevents execution of the code inside
    `draw()` and the user can manipulate the screen contents through
    event handlers like `mouse_pressed()`, etc.

    """
    default_sketch.looping = False

def loop():
    """Make sure `draw()` is being called continuously.

    `loop()` reverts the effects of `no_loop()` and allows `draw()` to
    be called continously again.

    """
    default_sketch.looping = True

def redraw():
    """Call `draw()` once.

    If looping has been disabled using `no_loop()`, `redraw()` will
    make sure that `draw()` is called *exactly* once.

    """
    if not default_sketch.looping:
        default_sketch.redraw = True

def exit(*args, **kwargs):
    """Exit the sketch.

    `exit()` overrides Python's builtin exit() function and makes sure
    that necessary cleanup steps are performed before exiting the
    sketch.

    :param args: positional argumets to pass to Python's builtin
        `exit()` function.

    :param kwargs: keyword-arguments to pass to Python's builtin
        `exit()` function.
    """
    default_sketch.show(visible=False)
    app.quit()
    builtins.exit(*args, **kwargs)

def no_cursor():
    """Hide the mouse cursor.
    """
    # window.set_mouse_visible(False)
    raise NotImplementedError

def cursor(cursor_type='ARROW'):
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
