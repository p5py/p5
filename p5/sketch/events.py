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

import builtins

from .base import window
from ..opengl import renderer

builtins.MOUSE_BUTTON = None
builtins.MOUSE_PRESSED = None
builtins.MOUSE_X = None
builtins.MOUSE_Y = None
builtins.PMOUSE_X = None
builtins.PMOUSE_Y = None
builtins.KEY = None
builtins.KEYCODE = None
builtins.KEY_PRESSED = None

@window.event
def on_exit():
    renderer.cleanup()
    window.close()

@window.event
def on_resize(width, height):
    renderer.reset_view()
    renderer.clear()
