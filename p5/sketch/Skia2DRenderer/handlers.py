"""
This file contains the handlers needed for glfw event handling
"""


import builtins
import glfw
from p5.core import p5
from p5.sketch.events import KeyEvent, MouseEvent

from dataclasses import dataclass
from time import time

from p5.util import keys

BUTTONMAP = {
    glfw.MOUSE_BUTTON_LEFT: 1,
    glfw.MOUSE_BUTTON_RIGHT: 2,
    glfw.MOUSE_BUTTON_MIDDLE: 3,
}


KEYMAP = {
    glfw.KEY_LEFT_SHIFT: keys.SHIFT,
    glfw.KEY_RIGHT_SHIFT: keys.SHIFT,
    glfw.KEY_LEFT_CONTROL: keys.CONTROL,
    glfw.KEY_RIGHT_CONTROL: keys.CONTROL,
    glfw.KEY_LEFT_ALT: keys.ALT,
    glfw.KEY_RIGHT_ALT: keys.ALT,
    glfw.KEY_LEFT_SUPER: keys.META,
    glfw.KEY_RIGHT_SUPER: keys.META,
    glfw.KEY_LEFT: keys.LEFT,
    glfw.KEY_UP: keys.UP,
    glfw.KEY_RIGHT: keys.RIGHT,
    glfw.KEY_DOWN: keys.DOWN,
    glfw.KEY_PAGE_UP: keys.PAGEUP,
    glfw.KEY_PAGE_DOWN: keys.PAGEDOWN,
    glfw.KEY_INSERT: keys.INSERT,
    glfw.KEY_DELETE: keys.DELETE,
    glfw.KEY_HOME: keys.HOME,
    glfw.KEY_END: keys.END,
    glfw.KEY_ESCAPE: keys.ESCAPE,
    glfw.KEY_BACKSPACE: keys.BACKSPACE,
    glfw.KEY_F1: keys.F1,
    glfw.KEY_F2: keys.F2,
    glfw.KEY_F3: keys.F3,
    glfw.KEY_F4: keys.F4,
    glfw.KEY_F5: keys.F5,
    glfw.KEY_F6: keys.F6,
    glfw.KEY_F7: keys.F7,
    glfw.KEY_F8: keys.F8,
    glfw.KEY_F9: keys.F9,
    glfw.KEY_F10: keys.F10,
    glfw.KEY_F11: keys.F11,
    glfw.KEY_F12: keys.F12,
    glfw.KEY_SPACE: keys.SPACE,
    glfw.KEY_ENTER: keys.ENTER,
    "\r": keys.ENTER,
    glfw.KEY_TAB: keys.TAB,
}

MOD_KEYS = [keys.SHIFT, keys.ALT, keys.CONTROL, keys.META]


@dataclass
class InputState:
    """
    A class to store the current state of Input
    """

    modifiers: list
    last_mouse_clicked_time: float
    next_key_events: list
    next_key_text: dict

    def process_mod(self, key, down):
        """Process (possible) keyboard modifiers"""
        if key in MOD_KEYS:
            if down:
                if key not in self.modifiers:
                    self.modifiers.append(key)
            elif key in self.modifiers:
                self.modifiers.pop(self.modifiers.index(key))
        return self.modifiers

    def process_key(self, key):
        if 32 <= key <= 127:
            return keys.Key(chr(key)), chr(key)
        elif key in KEYMAP:
            return KEYMAP[key], ""
        else:
            return None, ""


class PseudoKeyEvent:
    """Class to pass pseudo event data. They are used to work with the events module which is vispy dependent"""

    def __init__(self, key=None, mod=None, text=None):
        self.key = key
        self.modifiers = mod
        self.text = text


class PseudoMouseEvent:
    """
    Class to pass pseudo event data. They are used to work with the events module which is vispy dependent
    """

    def __init__(
        self, pos=(0, 0), delta=(0, 0), modifiers=None, button=None, buttons=None
    ):
        """Initialize the pseduoMouseEventClass to work with exisiting event system

        Args:
            pos (tuple): Position of the cursor
            delta (tuple): The increment by which the mouse wheel has moved
            modifiers (list): Modifiers active during the event
            button (int): Mouse Button that was pressed
            buttons (list): Mouse Buttons that were pressed during the event
        """
        self.pos = pos
        self.delta = delta
        self.modifiers = modifiers
        self.button = button
        self.buttons = buttons


# Hold the input state for current sketch
input_state = InputState([], 0, [], {})


def on_mouse_button(window, button, action, mod):
    pos = glfw.get_cursor_pos(window)

    if button < 3:
        button = BUTTONMAP.get(button, 0)

    event = PseudoMouseEvent(pos, (0, 0), input_state.modifiers, button, [])
    mev = MouseEvent(event, active=(action == glfw.PRESS))

    if action == glfw.PRESS:
        p5.sketch._enqueue_event("mouse_pressed", mev)
    else:
        p5.sketch._enqueue_event("mouse_released", mev)
        p5.sketch._enqueue_event("mouse_clicked", mev)

        dt_max = 0.3  # time in seconds for a double-click detection
        if time() - input_state.last_mouse_clicked_time <= dt_max:
            p5.sketch._enqueue_event("mouse_double_clicked", mev)

        input_state.last_mouse_clicked_time = time()


def on_mouse_scroll(window, x_off, y_off):
    pos = glfw.get_cursor_pos(window)
    delta = (float(x_off), float(y_off))
    event = PseudoMouseEvent(pos=pos, delta=delta, modifiers=input_state.modifiers)
    mev = MouseEvent(event, active=builtins.mouse_is_pressed)

    p5.sketch._enqueue_event("mouse_wheel", mev)


def on_mouse_motion(window, x, y):
    event = PseudoMouseEvent(pos=(x, y), modifiers=input_state.modifiers)
    mev = MouseEvent(event, active=builtins.mouse_is_pressed)

    # Queue a 'mouse_dragged` or `mouse_moved` event, not both similar to p5.js
    p5.sketch._enqueue_event(
        "mouse_dragged" if builtins.mouse_is_pressed else "mouse_moved", mev
    )


def on_key_press(window, key, scancode, action, mod):
    key, text = input_state.process_key(key)
    if action == glfw.PRESS:
        down = True
    elif action == glfw.RELEASE:
        down = False
    else:
        return
    input_state.process_mod(key, down=down)

    # NOTE: GLFW only provides localized characters via _on_key_char, so if
    # this event contains a character we store all other data and dispatch
    # it once the final unicode character is sent shortly after.
    if text != "" and action == glfw.PRESS:
        input_state.next_key_events.append((action, key, input_state.modifiers))
    else:
        if key in input_state.next_key_text:
            text = input_state.next_key_text[key]
            del input_state.next_key_text[key]
        # Not a char event, call the event normally
        event = PseudoKeyEvent(key, input_state.modifiers, text)
        kev = KeyEvent(event, action == glfw.PRESS)
        p5.sketch._enqueue_event(
            "key_pressed" if action == glfw.PRESS else "key_released", kev
        )


def on_key_char(window, text):
    # Repeat strokes (frequency configured at OS) are sent here only,
    # no regular _on_key_press events. Currently ignored!
    if len(input_state.next_key_events) == 0:
        return

    (action, key, mod) = input_state.next_key_events.pop(0)
    input_state.next_key_text[key] = text

    event = PseudoKeyEvent(key, mod, chr(text))
    kev = KeyEvent(event, action == glfw.PRESS)

    p5.sketch._enqueue_event(
        "key_pressed" if action == glfw.PRESS else "key_released", kev
    )


def on_window_focus(window, focused):
    builtins.focused = bool(focused)


def on_close(window):
    pass
