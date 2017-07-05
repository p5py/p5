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
from collections import namedtuple

import pyglet
from pyglet.window import mouse
from pyglet.window import key

from . import base
from .base import handlers
from .base import renderer
from .base import window

builtins.focused = True
builtins.mouse_button = None
builtins.mouse_is_pressed = False
builtins.mouse_is_dragging = False
builtins.mouse_x = 0
builtins.mouse_y = 0
builtins.pmouse_x = 0
builtins.pmouse_y = 0

builtins.MOUSE_LEFT = mouse.LEFT
builtins.MOUSE_CENTER = mouse.MIDDLE
builtins.MOUSE_RIGHT = mouse.RIGHT

builtins.key = None
builtins.key_code = None
builtins.key_pressed = None

Position = namedtuple('Position', ['x', 'y'])

class Event:
    def __init__(self, modifiers):
        self.modifiers = modifiers

    def is_shift_down(self):
        """Was shift held down during the event?

        :returns: True if the shift-key was held down.
        :rtype: bool

        """
        return self.modifiers & key.MOD_SHIFT

    def is_ctrl_down(self):
        """Was ctrl (command on Mac) held down during the event?

        :returns: True if the ctrl-key was held down.
        :rtype: bool

        """
        # MOD_ACCEL maps to MOD_COMMAND on Mac and to ctrl on windows
        # and X-systems.
        return self.modifiers & key.MOD_ACCEL

    def is_alt_down(self):
        """Was alt held down during the event?

        :returns: True if the alt-key was held down.
        :rtype: bool

        :note: This isn't available on a Mac.

        """
        return self.modifiers & key.MOD_ALT

    def is_meta_down(self):
        """Was the meta key (windows/option key) held down?

        :returns: True if the meta-key was held down.
        :rtype: bool

        """
        win_pressed = self.modifiers & key.MOD_WINDOWS
        option_pressed = self.modifiers & keys.MOD_OPTION
        return  win_pressed or option_pressed

    def _update_globals(self):
        """Update global variables associated with this event."""
        raise NotImplementedError("abstract")

    def _add_to_handler_queue(self):
        """Add the current event to the main handler queue."""
        raise NotImplementedError("abstract")


class MouseButton:
    """A simple class to work with mouse buttons."""
    def __init__(self, buttons):
        self._buttons = buttons

    def __eq__(self, other):
        if other in [mouse.LEFT, mouse.MIDDLE, mouse.RIGHT]:
            return self._buttons & other
        return self._buttons == other._buttons

    def __repr__(self):
        return mouse.buttons_string(self._buttons)

    __str__ = __repr__


class MouseEvent(Event):
    """A class that encapsulates information about a mouse event.

    :param action: The action type for the mouse event. One of
        {'PRESS', 'RELEASE', 'CLICK', 'DRAG', 'MOVE', 'ENTER', 'EXIT',
        'WHEEL'}
    :type action: str

    :param x: The x-position of the mouse in the window at the time of
        the event.
    :type x: int

    :param y: The y-position of the mouse in the window at the time of
        the event.
    :type y: int

    :param change: the change in the x and y directions (defaults to
        (0, 0))
    :type change: 2-tuple

    :param scroll: the scroll amount in the x and y directions
         (defaults to (0, 0)).
    :type scroll: 2-tuple

    :param buttons: The mouse buttons that were pressed at the time of
         the event.
    :type buttons: int

    :param modifiers: The modifier keys pressed at the time of the
        event.
    :type modifiers: int

    :param handler_name: The name of the handler to be attached to the
        current event.
    :type handler_name: str

    """
    def __init__(self, action, x, y, change=(0, 0), scroll=(0, 0),
                 buttons=None, modifiers=0, handler_name=None):
        self.position = Position(x, y)
        self.change = Position(*change)
        self.scroll = Position(*scroll)
        self.x = x
        self.y = y
        self.count = self.scroll.y
        self.action = action
        self.modifiers = modifiers
        if buttons is not None:
            self.button = MouseButton(buttons)
        else:
            self.button = None

        if handler_name is not None:
            self.handler_name = handler_name
        else:
            if self.action.endswith('E'):
                self.handler_name = "mouse_{}d".format(action.lower())
            else:
                self.handler_name = "mouse_{}ed".format(action.lower())

        self._update_globals()
        self._add_to_handler_queue()

    def _update_globals(self):
        builtins.pmouse_x = builtins.mouse_x
        builtins.pmouse_y = builtins.mouse_y
        builtins.mouse_x = self.x
        builtins.mouse_y = self.y
        builtins.mouse_button = self.button

    def _add_to_handler_queue(self):
        if self.handler_name in base.handler_names:
            base.handler_queue.append((handlers[self.handler_name], self))

    def __repr__(self):
        button_string = 'NO' if self.button is None else str(self.button)
        fvalues = self.action, self.position, button_string
        return "MouseEvent( {} at {} with {} button(s) )".format(*fvalues)

    __str__ = __repr__

@window.event
def on_exit():
    renderer.cleanup()
    window.close()

@window.event
def on_resize(width, height):
    renderer.reset_view()
    renderer.clear()

@window.event
def on_mouse_enter(x, y):
    event = MouseEvent('ENTER', x, y)

@window.event
def on_mouse_leave(x, y):
    event = MouseEvent('EXIT', x, y)

@window.event
def on_mouse_motion(x, y, dx, dy):
    event = MouseEvent('MOVE', x, y, change=(dx, dy))

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    builtins.mouse_is_dragging = True
    event = MouseEvent('DRAG', x, y, change=(dx, dy), buttons=buttons,
                       modifiers=modifiers, handler_name='mouse_dragged')

@window.event
def on_mouse_press(x, y, button, modifiers):
    builtins.mouse_is_pressed = True
    event = MouseEvent('PRESS', x, y, buttons=button, modifiers=modifiers)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    builtins.mouse_is_dragging = False
    builtins.mouse_is_pressed = False
    event = MouseEvent('RELEASE', x, y, buttons=buttons, modifiers=modifiers)
    event = MouseEvent('CLICK', x, y, buttons=buttons, modifiers=modifiers)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    event = MouseEvent('WHEEL', x, y, scroll=(scroll_x, scroll_y),
                       handler_name='mouse_wheel')

@window.event
def on_key_press(symbol, modifiers):
    builtins.key = symbol
    builtins.key_code = modifiers
    builtins.key_pressed = True
    event = Event(modifiers)
    base.handler_queue.append((handlers['key_pressed'], event))

@window.event
def on_key_release(symbol, modifiers):
    builtins.key = symbol
    builtins.key_code = modifiers
    builtins.key_pressed = False
    event = Event(modifiers)
    base.handler_queue.append((handlers['key_released'], event))

@window.event
def on_text(text):
    event = Event(modifiers)
    base.handler_queue.append((handlers['key_typed'], event))

@window.event
def on_activate():
    builtins.focused = True

@window.event
def on_deactivate():
    builtins.focused = False
