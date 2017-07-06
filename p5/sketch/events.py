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

builtins.key = None
builtins.key_is_pressed = False

Position = namedtuple('Position', ['x', 'y'])

class Event:
    def __init__(self, modifiers, handler_name=None):
        self.modifiers = modifiers
        self.handler_name = handler_name

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
        if self.handler_name in base.handler_names:
            base.handler_queue.append((handlers[self.handler_name], self))

    @staticmethod
    def _generate_hander_name(prefix, action):
        """Generate a handler name from a prefix and action.
        """
        if action.upper().endswith('E'):
            return "{}_{}d".format(prefix, action.lower())
        else:
            return "{}_{}ed".format(prefix, action.lower())


class MouseButton:
    """A simple class to work with mouse buttons."""
    def __init__(self, buttons):
        self._buttons = buttons

    def __eq__(self, other):
        if isinstance(other, str):
            button_map = {
                'CENTER': mouse.MIDDLE,
                'MIDDLE': mouse.MIDDLE,
                'LEFT': mouse.LEFT,
                'RIGHT': mouse.RIGHT,
            }
            if other.upper() in button_map:
                return self._buttons & button_map[other.upper()]
            else:
                return False
        # What if the `other` is actually a MouseButton?
        # +- YES? Compare the _buttons!
        # +-- NO? Nothing to be done. Let the error bubble up...
        return self._buttons == other._buttons

    def __str__(self):
        return mouse.buttons_string(self._buttons)

    def __repr__(self):
        fvalues = self._buttons, str(self)
        return "MouseButton( code={}, buttons={} )".format(*fvalues)


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
        self.x = x
        self.y = builtins.height - y

        self.position = Position(self.x, self.y)
        self.change = Position(*change)
        self.scroll = Position(*scroll)

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
            self.handler_name = self._generate_hander_name('mouse', action)

        self._update_globals()
        self._add_to_handler_queue()

    def _update_globals(self):
        builtins.pmouse_x = builtins.mouse_x
        builtins.pmouse_y = builtins.mouse_y
        builtins.mouse_x = self.x
        builtins.mouse_y = self.y
        builtins.mouse_button = self.button
        if self.action == 'PRESS':
            builtins.mouse_is_pressed = True
        elif self.action == 'DRAG':
            builtins.mouse_is_dragging = True
        elif self.action == 'RELEASE':
            builtins.mouse_is_pressed = False
            builtins.mouse_is_dragging = False

    def __repr__(self):
        button_string = 'NO' if self.button is None else str(self.button)
        fvalues = self.action, self.position, button_string
        return "MouseEvent( {} at {} with {} button(s) )".format(*fvalues)

    __str__ = __repr__


class Key:
    """A higher level abstraction over a single key press.

    :param key_code: The key_code symbol for this key (should be a
        symbol defined in pyglet.window.key)
    :type key_code: int

    """
    def __init__(self, key_code):
        self._key_code = key_code

    def __eq__(self, other):
        if isinstance(other, str):
            # to check if two keys are equal, we get the equivalent
            # attribute form pyglet.window.key and then compare the
            # key codes.
            if hasattr(key, other.upper()):
                other_key = getattr(key, other.upper())
                return other_key == self._key_code
            # the numeric keys in pyglet.window.key are prefixed with
            # an underscrore. This workaround makes sure that we check
            # if a numeric key is pressed when the first condition
            # fails.
            elif hasattr(key, '_' + other):
                other_key = get_attr(key, '_' + other)
                return other_key == self._key_code
            else:
                return False
        # maybe `other` is actually a Key?
        self._key_code == other._key_code

    def __str__(self):
        return key.symbol_string(self._key_code)

    def __repr__(self):
        return "Key( code={}, symbol={} )".format(self._key_code, str(self))


class KeyEvent(Event):
    """Encapsulates information about a key event.

    :param action: The action type for this key event. Should be one
        of {'PRESS', 'RELEASE', 'TYPE'}
    :type action: str

    :param key_text: The key-text for this event (defaults to None).
    :type key_text: str

    :param key_code: The symbol for the key that was pressed (defaults
        to None). This should be symbol defined in pyglet.window.key
    :param key_code: int

    :param modifiers: The modifier keys pressed at the time of the
        event.
    :type modifiers: int

    :param handler_name: The name of the handler function to be
        attached to this event (defaults to None). When this is not
        specified, KeyEvent automatically tried to generate a function
        name to use using the `action` string.
    :type handler_name: str

    :raises ValueError: When both key_text and key_code are None
        during initialization.

    """
    def __init__(self, action, key_text=None, key_code=None,
                 modifiers=0, handler_name=None):

        self.action = action

        if key_text is not None:
            self.key = key_text
        elif key_code is not None:
            self.key = Key(key_code)
        else:
            raise ValueError('Failed to assign a key to the event!')

        if handler_name is not None:
            self.handler_name = handler_name
        else:
            self.handler_name = self._generate_hander_name('key', action)

        self._update_globals()
        self._add_to_handler_queue()

    def _update_globals(self):
        builtins.key = self.key
        if self.action == 'PRESS':
            builtins.key_is_pressed = True
        elif self.action == 'RELEASE':
            builtins.key_is_pressed = False

    def __repr__(self):
        return "KeyEvent( {} key {} )".format(self.action, str(self.key))

    __str__ = __repr__

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
    event = MouseEvent('DRAG', x, y, change=(dx, dy), buttons=buttons,
                       modifiers=modifiers, handler_name='mouse_dragged')

@window.event
def on_mouse_press(x, y, button, modifiers):
    event = MouseEvent('PRESS', x, y, buttons=button, modifiers=modifiers)

@window.event
def on_mouse_release(x, y, buttons, modifiers):
    event = MouseEvent('RELEASE', x, y, buttons=buttons, modifiers=modifiers)
    event = MouseEvent('CLICK', x, y, buttons=buttons, modifiers=modifiers)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    event = MouseEvent('WHEEL', x, y, scroll=(scroll_x, scroll_y),
                       handler_name='mouse_wheel')

@window.event
def on_key_press(symbol, modifiers):
    event = KeyEvent('PRESS', key_code=symbol, modifiers=modifiers)

@window.event
def on_key_release(symbol, modifiers):
    event = KeyEvent('RELEASE', key_code=symbol, modifiers=modifiers)

@window.event
def on_text(text):
    event = KeyEvent('TYPE', key_text=text)

@window.event
def on_activate():
    builtins.focused = True

@window.event
def on_deactivate():
    builtins.focused = False

@window.event
def on_exit():
    renderer.cleanup()
    window.close()

@window.event
def on_resize(width, height):
    renderer.reset_view()
    renderer.clear()
