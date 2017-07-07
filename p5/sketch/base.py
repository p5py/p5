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

import builtins
from functools import wraps

import __main__

import pyglet

from ..opengl import renderer

builtins.width = 800
builtins.height = 600
builtins.title = "p5"
builtins.frame_count = -1
builtins.frame_rate = 30

# builtins.PIXEL_HEIGHT = None
# builtins.PIXEL_WIDTH = None

platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()

# We really want some antialiasing. So, keep trying.
template = pyglet.gl.Config(samples_buffers=1, samples=4)
try:
    config = screen.get_best_config(template)
except pyglet.window.NoSuchConfigException:
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
    config=config
)

window.set_minimum_size(100, 100)

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
target_frame_rate = 60.0

def draw():
    pass

def setup():
    pass

fps_display = pyglet.clock.ClockDisplay()

def update(dt):
    global handler_queue
    global redraw
    global setup_done

    builtins.frame_count += 1
    builtins.frame_rate = int(1 / (dt + 0.0001))

    renderer.pre_render()
    if not setup_done:
        setup()
        setup_done = True
    if looping or redraw:
        draw()
        redraw = False
    for function, event in handler_queue:
        function(event)
    handler_queue = []
    renderer.post_render()

def no_loop():
    global _looping
    _looping = False

def loop():
    global _looping
    _looping = True

def redraw():
    global _redraw
    if not _looping:
        _redraw = True

def size(width, height):
    """Resize the window.

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
    window.set_caption("{} - p5".format(new_title))

def no_cursor():
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

def initialize(*args, **kwargs):
    renderer.initialize(window.context)
    window.set_visible()

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

def run(user_setup=None, user_draw=None):
    """Run a sketch.
    """
    global draw
    global setup

    if user_setup is not None:
        setup = user_setup
    elif hasattr(__main__, 'setup'):
        setup = __main__.setup

    if user_draw is not None:
        draw = user_draw
    elif hasattr(__main__, 'draw'):
        draw = __main__.draw

    for handler in handler_names:
        if hasattr(__main__, handler):
            handler_func = getattr(__main__, handler)
            handlers[handler] = fix_handler_interface(handler_func)

    initialize()
    pyglet.clock.schedule_interval(update, 1/(target_frame_rate + 1))
    pyglet.app.run()

def artist(f):
    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.
    @wraps(f)
    def decorated(*args, **kwargs):
        shape = f(*args, **kwargs)
        renderer.render(shape)
        return shape
    return decorated

def exit(*args, **kwargs):
    """Override the system exit to make sure we perform necessary
        cleanups, etc.
    """
    pyglet.app.exit()
    builtins.exit(*args, **kwargs)

def test_run():
    initialize()
    def tester(dt):
        renderer.pre_render()
        renderer.test_render()
        renderer.post_render()
    pyglet.clock.schedule(tester)
    pyglet.app.run()
