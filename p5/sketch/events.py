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

import pyglet

from . import base
from .base import window
from .base import handlers
from ..opengl import renderer

builtins.FOCUSED = True
builtins.MOUSE_BUTTON = None
builtins.MOUSE_PRESSED = False
builtins.MOUSE_X = 0
builtins.MOUSE_Y = 0
builtins.PMOUSE_X = 0
builtins.PMOUSE_Y = 0
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

def _update_mouse_coords(new_x, new_y):
    builtins.PMOUSE_X = builtins.MOUSE_X
    builtins.PMOUSE_Y = builtins.MOUSE_Y
    builtins.MOUSE_X = new_x
    builtins.MOUSE_Y = new_y

@window.event
def on_mouse_enter(x, y):
    _update_mouse_coords(x, y)

@window.event
def on_mouse_leave(x, y):
    _update_mouse_coords(x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    _update_mouse_coords(x, y)
    builtins.KEY_CODE = modifiers
    base.handler_queue.append(handlers['mouse_dragged'])

@window.event
def on_mouse_motion(x, y, dx, dy):
    _update_mouse_coords(x, y)
    base.handler_queue.append(handlers['mouse_moved'])

@window.event
def on_mouse_press(x, y, button, modifiers):
    _update_mouse_coords(x, y)
    builtins.KEY_CODE = modifiers
    builtins.MOUSE_PRESSED = True
    base.handler_queue.append(handlers['mouse_pressed'])

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    _update_mouse_coords(x, y)
    builtins.KEY_CODE = modifiers
    builtins.MOUSE_PRESSED = False
    base.handler_queue.append(handlers['mouse_released'])
    base.handler_queue.append(handlers['mouse_clicked'])

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    _update_mouse_coords(x, y)
    base.handler_queue.append(handlers['mouse_wheel'])

@window.event
def on_key_press(symbol, modifiers):
    builtins.KEY = symbol
    builtins.KEY_CODE = modifiers
    builtins.KEY_PRESSED = True
    base.handler_queue.append(handlers['key_pressed'])

@window.event
def on_key_release(symbol, modifiers):
    builtins.KEY = symbol
    builtins.KEY_CODE = modifiers
    builtins.KEY_PRESSED = False
    base.handler_queue.append(handlers['key_released'])

@window.event
def on_text(text):
    base.handler_queue.append(handlers['key_typed'])

@window.event
def on_activate():
    builtins.FOCUSED = True

@window.event
def on_deactivate():
    builtins.FOCUSED = False
