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

_min_width = 100
_min_height = 100

builtins.WIDTH = 800
builtins.HEIGHT = 600
builtins.TITLE = "p5py"
builtins.FRAME_COUNT = -1
builtins.FRAME_RATE = None

# builtins.PIXEL_HEIGHT = None
# builtins.PIXEL_WIDTH = None

window = pyglet.window.Window(
    width=WIDTH,
    height=HEIGHT,
    caption=TITLE,
    resizable=False,
    visible=False,
    vsync=False
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

def _draw():
    pass

def _setup():
    pass

def initialize(*args, **kwargs):
    gl_version = window.context.get_info().get_version()[:3]
    renderer.initialize(gl_version)
    window.set_visible()

def size(width, height):
    """Resize the window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.WIDTH = int(width)
    builtins.HEIGHT = int(height)
    window.set_size(width, height)

def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    window.set_caption("{} - p5".format(new_title))

def run(setup=None, draw=None):
    """Run a sketch.
    """
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)

    global _draw
    global _setup

    if setup is not None:
        _setup = setup
    elif hasattr(__main__, 'setup'):
        _setup = __main__.setup

    if draw is not None:
        _draw = draw
    elif hasattr(__main__, 'draw'):
        _draw = __main__.draw

    for handler in handler_names:
        if hasattr(__main__, handler):
            handlers[handler] = getattr(__main__, handler)

    def update(dt):
        builtins.FRAME_COUNT += 1

    initialize()
    pyglet.clock.schedule_interval(update, 1/30.0)
    pyglet.app.run()

@window.event
def on_draw():
    global handler_queue
    pyglet.clock.tick()
    renderer.pre_render()
    if FRAME_COUNT == 0:
        _setup()
    _draw()
    for handler_function in handler_queue:
        handler_function()
    handler_queue = []
    renderer.post_render()

def artist(f):
    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @_p5_artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.
    @wraps(f)
    def decorated(*args, **kwargs):
        shape = f(*args, **kwargs)
        renderer.render(shape)
        return shape
    return decorated

def test_run():
    initialize()
    def tester(dt):
        renderer.pre_render()
        renderer.test_render()
        renderer.post_render()
    pyglet.clock.schedule(tester)
    pyglet.app.run()
