#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Base module for a sketch."""

import __main__
import builtins
from functools import wraps
import time

import pyglet
pyglet.options["shadow_window"] = False

from ..opengl import renderer

__all__ = ['setup', 'draw', 'run', 'no_loop', 'loop', 'redraw', 'size',
           'title', 'no_cursor', 'cursor', 'exit',]

builtins.width = 360
builtins.height = 360
builtins.title = "p5"
builtins.frame_count = -1
builtins.frame_rate = 30
last_recorded_time = time.time()

builtins.pixel_width = 1
builtins.pixel_height = 1

platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()

template = pyglet.gl.Config(samples_buffers=1, samples=2)
try:
    config = screen.get_best_config(template)
except pyglet.window.NoSuchConfigException:
    template = pyglet.gl.Config()
    config = screen.get_best_config(template)

window = pyglet.window.Window(
    width=builtins.width,
    height=builtins.height,
    caption=builtins.title,
    resizable=False,
    visible=False,
    vsync=False,
    config=config,
)

window.set_minimum_size(100, 100)

# DO NOT REMOVE THIS
#
# We tried removing this line and things broke badly on Mac machines.
# We still don't know why. Let's just keep this here for now.
_ = pyglet.clock.ClockDisplay()

def _dummy_handler(*args, **kwargs):
    return pyglet.event.EVENT_HANDLED

handler_names = [ 'key_press', 'key_pressed', 'key_released',
                  'key_typed', 'mouse_clicked', 'mouse_dragged',
                  'mouse_moved', 'mouse_pressed', 'mouse_released',
                  'mouse_wheel',]

handlers =  dict.fromkeys(handler_names, _dummy_handler)

handler_queue = []

looping = True
redraw = False
setup_done = False

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

def no_loop():
    """Stop draw() from being continuously called.

    By default, the sketch continuously calls `draw()` as long as it
    runs. Calling `no_loop()` stops draw() from being called the next
    time. Note that this only prevents execution of the code inside
    `draw()` and the user can manipulate the screen contents through
    event handlers like `mouse_pressed()`, etc.

    """
    global looping
    looping = False

def loop():
    """Make sure `draw()` is being called continuously.

    `loop()` reverts the effects of `no_loop()` and allows `draw()` to
    be called continously again.

    """
    global looping
    looping = True

def redraw():
    """Call `draw()` once.

    If looping has been disabled using `no_loop()`, `redraw()` will
    make sure that `draw()` is called *exactly* once.

    """
    global redraw
    if not looping:
        redraw = True

def size(width, height):
    """Resize the sketch window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.width = int(width)
    builtins.height = int(height)
    window.set_size(width, height)

def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    builtins.title = new_title
    window.set_caption(str(new_title))

def no_cursor():
    """Hide the mouse cursor.
    """
    window.set_mouse_visible(False)

def cursor(cursor_type='ARROW'):
    """Set the cursor to the specified type.

    :param cursor_type: The cursor type to be used (defaults to
        'ARROW'). Should be one of: {'ARROW','CROSS','HAND', 'MOVE',
        'TEXT', 'WAIT'}
    :type cursor_type: str

    """
    cursor_map = {
        'ARROW': window.CURSOR_DEFAULT,
        'CROSS': window.CURSOR_CROSSHAIR,
        'HAND': window.CURSOR_HAND,
        'MOVE': window.CURSOR_SIZE,
        'TEXT': window.CURSOR_TEXT,
        'WAIT': window.CURSOR_WAIT
    }
    selected_cursor = cursor_map.get(cursor_type, 'ARROW')
    cursor = window.get_system_mouse_cursor(selected_cursor)
    window.set_mouse_visible(True)
    window.set_mouse_cursor(cursor)

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
    pyglet.app.exit()
    builtins.exit(*args, **kwargs)

@window.event
def on_draw():
    pass

def update(dt):
    global handler_queue
    global redraw
    global setup_done
    global last_recorded_time

    with renderer.draw_loop():
        if looping or redraw:
            builtins.frame_count += 1
            now = time.time()
            builtins.frame_rate = 1 / (now - last_recorded_time)
            last_recorded_time = now
            if not setup_done:
                setup()
                setup_done = True
                if not window.visible:
                    window.set_visible(True)
            else:
                draw()
                redraw = False
        for function, event in handler_queue:
            function(event)
        handler_queue = []

def fix_handler_interface(func):
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
    global draw
    global setup

    if sketch_setup is not None:
        setup = sketch_setup
    elif hasattr(__main__, 'setup'):
        setup = __main__.setup

    if sketch_draw is not None:
        draw = sketch_draw
    elif hasattr(__main__, 'draw'):
        draw = __main__.draw

    for handler in handler_names:
        if hasattr(__main__, handler):
            handler_func = getattr(__main__, handler)
            handlers[handler] = fix_handler_interface(handler_func)

    renderer.initialize(window.context)
    pyglet.clock.schedule_interval(update, 1 / max(frame_rate, 1))
    pyglet.app.run()


def draw_shape(shape):
    """Handle the lower level stuff associated with drawing a shape.

    :param shape: The shape to be drawn.
    :type shape: Shape

    """
    # TODO (abhikpal 2017-08-05)
    #
    # Add a check that insures that we don't call the renderer
    # directly while drawing a shape.
    renderer.render(shape)
