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

from functools import wraps
import pyglet

from ..opengl import renderer

title = "p5py"
min_width = 100
min_height = 100
width = 800
height = 600

window = pyglet.window.Window(
    width=width,
    height=height,
    caption=title,
    resizable=False,
    vsync=True,
    visible=False,
)

def initialize(*args, **kwargs):
    gl_version = window.context.get_info().get_version()[:3]
    renderer.initialize(width, height, gl_version)
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

def test_run():
    initialize()
    def tester(dt):
        renderer.pre_render()
        renderer.test_render()
        renderer.post_render()
    pyglet.clock.schedule(tester)
    pyglet.app.run()
    
def update(dt):
    renderer.pre_render()
    renderer.post_render()

