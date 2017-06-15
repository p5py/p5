#
# Part of p5py: A Python package based on Processing
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

from collections import deque
from functools import wraps

import pyglet

# This should only have the relevant sketch contants.
__all__ = []

title = "p5py"
min_width = 100
min_height = 100
width = 800
height = 600

background_color = None
fill_color = None
stroke_color = None

fill_enabled = True
stroke_enabled = True

mat_projection = None
mat_view = None
model_matrix_stack = deque()

window = pyglet.window.Window(
    width=width,
    height=height,
    caption=title,
    resizable=False,
    vsync=True,
)

debug = True
gl_version = window.context.get_info().get_version()[:3]

renderer = None

def initialize(*args, **kwargs):
    window.set_visible()

def run(*args, **kwargs):
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)
    pyglet.clock.schedule(update)
    pyglet.app.run()

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

def update(dt):
    renderer.pre_render()
    renderer.test_render()
    renderer.post_render()

@window.event
def on_exit():
    renderer.cleanup()
    window.close()

from .opengl import OpenGLRenderer
renderer = OpenGLRenderer()
renderer.initialize()
