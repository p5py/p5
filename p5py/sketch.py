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

_attrs = {
    'title': "p5py",
    'width': 800,
    'min_width': 100,
    'height': 600,
    'min_height': 100,

    'background_color': None,
    'fill_color': None,
    'stroke_color': None,

    'fill_enabled': True,
    'stroke_enabled': True,

    'debug': False,
    'gl_version': None,
}

_window = None
_renderer = None

def _initialize(*args, **kwargs):
    _window.set_visible()

def _run(*args, **kwargs):
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)
    pyglet.clock.schedule(_update)
    pyglet.app.run()

def _artist(f):
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

def _update(dt):
    _renderer.clear()
    _renderer.test_render()

from .backends import OpenGLRenderer

_window = pyglet.window.Window(
    width=_attrs['width'],
    height=_attrs['height'],
    caption=_attrs['title'],
    resizable=False,
    vsync=True,
)

_renderer = OpenGLRenderer()
_renderer.initialize()

_gl_version_string = _window.context.get_info().get_version()
_attrs['gl_version'] = _gl_version_string[:3]

@_window.event
def on_exit():
    _renderer.cleanup()
    _window.close()
