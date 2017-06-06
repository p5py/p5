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

from functools import wraps

import pyglet

from .backends import OpenGLRenderer

_attrs = {
    'title': "p5py",
    'width': 800,
    'min_width': 100,
    'height': 600,
    'min_height': 100,

    'background_color': (0.9, 0.9, 0.9, 1.0),
    'fill_color': (0.5, 0.5, 0.5, 1.0),
    'stroke_color': (0.2, 0.2, 0.2, 1.0),
}

_window = pyglet.window.Window(
    width=_attrs['width'],
    height=_attrs['height'],
    caption=_attrs['title'],
    resizable=False,
    visible=False,
)

_renderer = OpenGLRenderer(sketch_attrs=_attrs)
_renderer.initialize()

def _initialize(*args, **kwargs):
    _window.set_visible()

def _run(*args, **kwargs):
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)
    pyglet.clock.schedule(update)
    pyglet.app.run()

def _p5_attribute(f):
    # a decorator that will wrap around the "attribute setters" for
    # the sketch like fill, background, etc and modify internal state
    # variables.
    #
    #     @_p5_attribute
    #     def fill(*args, **kwargs):
    #         # code that returns a new color (after converting it
    #         # to the appropriate internal color object)
    return f

def _p5_transformation(f):
    # a decorator that will wrap around functions that control
    # transformations on the sketch. Like translate(), rotate(), etc.
    # 
    #    @_p5_transformation
    #    def translate(*args, **kwargs):
    #        # code that returns a matrix with the appropriate
    #        # translation applied to it.
    return f

def _p5_artist(f):
    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @_p5_artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.

    @wraps(f)
    def _artist(*args, **kwargs):
        shape = f(*args, **kwargs)
        _renderer.render(shape)
        return shape

    return _artist

@_window.event
def on_exit():
    _renderer.cleanup()
    _window.close()

def update(dt):
    _renderer.clear()
    _renderer.test_render()
    _window.flip()
