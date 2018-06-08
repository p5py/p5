#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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

import __main__
import builtins
from functools import wraps

import vispy
from vispy import app
from vispy import gloo

from collections import namedtuple
from enum import IntEnum

class VispyButton(IntEnum):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3

button_map = {
    'CENTER': VispyButton.MIDDLE,
    'MIDDLE': VispyButton.MIDDLE,
    'LEFT':  VispyButton.LEFT,
    'RIGHT': VispyButton.RIGHT,
}

button_inv_map = {
    VispyButton.LEFT: 'LEFT',
    VispyButton.RIGHT: 'RIGHT',
    VispyButton.MIDDLE: 'MIDDLE',
}

Position = namedtuple('Position', ['x', 'y'])
vispy.use('PyQt5')

# the global sketch instance.
default_sketch = None


# SKETCH GLOBALS =======================================================

builtins.width = 800
builtins.height = 600
builtins.title = "p5"

builtins.frame_count = -1

builtins.key_is_pressed = False

builtins.focused = False

builtins.pmouse_x = 0
builtins.pmouse_y = 0
builtins.mouse_x = 0
builtins.mouse_y = 0
builtins.mouse_button = None
builtins.mouse_is_pressed = False
builtins.mouse_is_dragging = False


# HELPER FUNCTIONS, ETC ================================================

handler_names = [ 'key_pressed', 'key_released', 'key_typed',
                  'mouse_clicked', 'mouse_double_clicked',
                  'mouse_dragged', 'mouse_moved',
                  'mouse_pressed', 'mouse_released', 'mouse_wheel',]

def fix_interface(func):
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

def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing.
    """
    pass

def reset_builtins():
    builtins.mouse_button = None
    builtins.mouse_is_pressed = False
    builtins.mouse_is_dragging = False

# SKETCH EVENTS ========================================================

class Event:
    def __init__(self, raw_event, active=False):
        self._modifiers = list(map(lambda k: k.name, raw_event.modifiers))
        self._active = active
        self._raw = raw_event

    def is_shift_down(self):
        """Was shift held down during the event?

        :returns: True if the shift-key was held down.
        :rtype: bool

        """
        return 'Shift' in self._modifiers

    def is_ctrl_down(self):
        """Was ctrl (command on Mac) held down during the event?

        :returns: True if the ctrl-key was held down.
        :rtype: bool

        """
        # MOD_ACCEL maps to MOD_COMMAND on Mac and to ctrl on windows
        # and X-systems.
        return 'Control' in self._modifiers

    def is_alt_down(self):
        """Was alt held down during the event?

        :returns: True if the alt-key was held down.
        :rtype: bool

        :note: This isn't available on a Mac.

        """
        return 'Alt' in self._modifiers

    def is_meta_down(self):
        """Was the meta key (windows/option key) held down?

        :returns: True if the meta-key was held down.
        :rtype: bool

        """
        return  'Meta' in self._modifiers

    def _update_builtins(self):
        pass

class KeyEvent(Event):
    def _update_builtins(self):
        builtins.key_is_pressed = self._active

class MouseButton:
    """A simple class to work with mouse buttons."""
    def __init__(self, buttons):
        self._buttons = buttons

    def __eq__(self, other):
        if isinstance(other, str):
            return button_map.get(other.upper(), -1) in self._buttons
        # What if the `other` is actually a MouseButton?
        # +- YES? Compare the _buttons!
        # +-- NO? Nothing to be done. Let the error bubble up...
        return self._buttons == other._buttons

    def __repr__(self):
        fstr = ', '.join(button_inv_map[bt] for bt in self._buttons)
        return "MouseButton({})".format(fstr)

    __str__ = __repr__

class MouseEvent(Event):
    """A class that encapsulates information about a mouse event.

    :param x: The x-position of the mouse in the window at the time of
        the event.
    :type x: int

    :param y: The y-position of the mouse in the window at the time of
        the event.
    :type y: int

    :param position: Position of the mouse in the window at the time
        of the event.
    :type position: (int, int)

    :param change: the change in the x and y directions (defaults to
        (0, 0))
    :type change: (int, int)

    :param scroll: the scroll amount in the x and y directions
         (defaults to (0, 0)).
    :type scroll: (int, int)

    :param count: amount by which the mouse whell was dragged.
    :type count: int

    :param button: Button information at the time of the event.
    :type button: MouseButton

    :param modifiers: The modifier keys pressed at the time of the
        event.
    :type modifiers: str list

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x, y = self._raw.pos
        y = builtins.height - y
        dx, dy = self._raw.delta

        if (self._raw.press_event != None) and (self._raw.last_event != None):
            px, py = self._raw.press_event.pos
            cx, cy = self._raw.last_event.pos
            self.change = Position(cx - px, cy - py)
        else:
            self.change = Position(0, 0)

        self.x = max(min(builtins.width, x), 0)
        self.y = max(min(builtins.height, builtins.height - y), 0)

        self.position = Position(x, y)
        self.scroll = Position(int(dx), int(dy))

        self.count = self.scroll.y
        self.button = MouseButton(self._raw.buttons)
        self.modifiers = self._modifiers

    def _update_builtins(self):
        builtins.pmouse_x = builtins.mouse_x
        builtins.pmouse_y = builtins.mouse_y
        builtins.mouse_x = self.x
        builtins.mouse_y = self.y
        builtins.mouse_button = self.button
        builtins.mouse_is_pressed = self._active
        builtins.mouse_is_dragging = (self.change == (0, 0))

    def __repr__(self):
        press = 'pressed' if self._active else 'not-pressed'
        return "MouseEvent({} at {})".format(press, self.position)

    __str__ = __repr__

# MAIN SKETCH CLASS ====================================================

class Sketch(app.Canvas):
    """The main sketch instance.
    """
    def __init__(self, *args, **kwargs):
        app.Canvas.__init__(self, *args, **kwargs)

        self.setup_method = lambda: None
        self.draw_method = lambda: None

        self.looping = True
        self.redraw = False
        self.setup_done = False
        self.timer = app.Timer('auto', connect=self.on_timer)

        self.handlers = dict.fromkeys(handler_names, _dummy)
        self.handler_queue = []

    def on_timer(self, event):
        if self.looping or self.redraw:
            builtins.frame_count += 1
            if not self.setup_done:
                self.setup_method()
                self.setup_done = True
                self.show(visible=True)
            else:
                self.draw_method()
                self.redraw = False
        self.update()

        # TODO: restore the previous state of builtins after dealing
        # with all the handlers.
        while len(self.handler_queue) != 0:
            function, event = self.handler_queue.pop(0)
            event._update_builtins()
            function(event)

    def on_close(self, event):
        exit()

    def on_draw(self, event):
        pass

    def on_resize(self, event):
        # we want programmers to be able to resize windows (using the
        # size() method), however, all user attempts to resize the
        # window should be ignored.
        pass

    def _enqueue_event(self, handler_name, event):
        event._update_builtins()
        self.handler_queue.append((self.handlers[handler_name], event))

    def on_key_press(self, event):
        self._enqueue_event('key_pressed', KeyEvent(event, active=True))

    def on_key_release(self, event):
        self._enqueue_event('key_released', KeyEvent(event))
        if not (event.text is ''):
            self._enqueue_event('key_typed', KeyEvent(event))

    def on_mouse_press(self, event):
        self._enqueue_event('mouse_pressed', MouseEvent(event, active=True))

    def on_mouse_double_click(self, event):
        self._enqueue_event('mouse_double_clicked', MouseEvent(event))

    def on_mouse_release(self, event):
        self._enqueue_event('mouse_released', MouseEvent(event))
        self._enqueue_event('mouse_clicked', MouseEvent(event))

    def on_mouse_move(self, event):
        self._enqueue_event('mouse_moved', MouseEvent(event))
        if builtins.mouse_is_pressed:
            self._enqueue_event('mouse_dragged', MouseEvent(event))

    def on_mouse_wheel(self, event):
        self._enqueue_event('mouse_wheel', MouseEvent(event))

    # def on_touch(self, event):
    #     self._enqueue_event('touch', event)

    # def on_stylus(self, event):
    #     self._enqueue_event('stylus', event)


# USER SPACE FUNCTIONS =================================================

def title(new_title):
    """Set the title of the p5 window.

    :param new_title: new title of the window.
    :type new_title: str

    """
    builtins.title = new_title
    default_sketch.title = new_title

def size(width, height):
    """Resize the sketch window.

    :param width: width of the sketch window.
    :type width: int

    :param height: height of the sketch window.
    :type height: int

    """
    builtins.width = int(width)
    builtins.height = int(height)
    default_sketch.size = (builtins.width, builtins.height)


def no_loop():
    """Stop draw() from being continuously called.

    By default, the sketch continuously calls `draw()` as long as it
    runs. Calling `no_loop()` stops draw() from being called the next
    time. Note that this only prevents execution of the code inside
    `draw()` and the user can manipulate the screen contents through
    event handlers like `mouse_pressed()`, etc.

    """
    default_sketch.looping = False

def loop():
    """Make sure `draw()` is being called continuously.

    `loop()` reverts the effects of `no_loop()` and allows `draw()` to
    be called continously again.

    """
    default_sketch.looping = True

def redraw():
    """Call `draw()` once.

    If looping has been disabled using `no_loop()`, `redraw()` will
    make sure that `draw()` is called *exactly* once.

    """
    if not default_sketch.looping:
        default_sketch.redraw = True

def draw():
    """Continuously execute code defined inside.

    The `draw()` function is called directly after `setup()` and all
    code inside is continuously executed until the program is stopped
    (using `exit()`) or `no_loop()` is called.

    """
    pass

def setup():
    """Called to setup initial sketch options.

    The `setup()` function is run once when the program starts and is
    used to define initial environment options for the sketch.

    """
    pass

def exit(*args, **kwargs):
    """Exit the sketch.

    `exit()` overrides Python's builtin exit() function and makes sure
    that necessary cleanup steps are performed before exiting the
    sketch.

    :param args: positional argumets to pass to Python's builtin
        `exit()` function.

    :param kwargs: keyword-arguments to pass to Python's builtin
        `exit()` function.
    """
    default_sketch.show(visible=False)
    app.quit()
    builtins.exit(*args, **kwargs)

def run(sketch_setup=None, sketch_draw=None, frame_rate=60):
    """Run a sketch.

    if no `sketch_setup` and `sketch_draw` are specified, p5 automatically
    "finds" the user-defined setup and draw functions.

    :param sketch_setup: The setup function of the sketch (None by
         default.)
    :type sketch_setup: function

    :param sketch_draw: The draw function of the sketch (None by
        default.)
    :type sketch_draw: function

    :param frame_rate: The target frame rate for the sketch.
    :type frame_rate: int :math:`\geq 1`

    """
    global default_sketch
    default_sketch = Sketch(
        title=builtins.title,
        size=(builtins.width, builtins.height),
        keys='interactive',
    )

    if sketch_setup is not None:
        default_sketch.setup_method = sketch_setup
    elif hasattr(__main__, 'setup'):
        default_sketch.setup_method = __main__.setup
    else:
        default_sketch.setup_method = setup

    if sketch_draw is not None:
        default_sketch.draw_method = sketch_draw
    elif hasattr(__main__, 'draw'):
        default_sketch.draw_method = __main__.draw
    else:
        default_sketch.draw_method = draw

    for handler in handler_names:
        if hasattr(__main__, handler):
            hfunc = getattr(__main__, handler)
            default_sketch.handlers[handler] = fix_interface(hfunc)

    # initialize the rendering engine.
    ...

    default_sketch.show()
    default_sketch.timer.start()

    ## TEST CODE - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    app.run()
    exit()

# USER SPACE (UN-IMPLEMENTED) ==========================================

def no_cursor():
    """Hide the mouse cursor.
    """
    # window.set_mouse_visible(False)
    raise NotImplementedError

def cursor(cursor_type='ARROW'):
    """Set the cursor to the specified type.

    :param cursor_type: The cursor type to be used (defaults to
        'ARROW'). Should be one of: {'ARROW','CROSS','HAND', 'MOVE',
        'TEXT', 'WAIT'}
    :type cursor_type: str

    """
    # cursor_map = {
    #     'ARROW': window.CURSOR_DEFAULT,
    #     'CROSS': window.CURSOR_CROSSHAIR,
    #     'HAND': window.CURSOR_HAND,
    #     'MOVE': window.CURSOR_SIZE,
    #     'TEXT': window.CURSOR_TEXT,
    #     'WAIT': window.CURSOR_WAIT
    # }
    # selected_cursor = cursor_map.get(cursor_type, 'ARROW')
    # cursor = window.get_system_mouse_cursor(selected_cursor)
    # window.set_mouse_visible(True)
    # window.set_mouse_cursor(cursor)
    raise NotImplementedError
