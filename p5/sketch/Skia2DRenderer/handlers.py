import builtins
from os import environ
import glfw
from p5.core import p5
from p5.sketch.events import MouseEvent

"""
This file contains the handlers needed for glfw event handling
"""

# TODO : Make a raw_event class and populate it with data about current events
# TODO : Design of raw_event should follow that of Vispy's raw event beacuse events.py is highly based on it  

BUTTONMAP = {glfw.MOUSE_BUTTON_LEFT: 1,
                glfw.MOUSE_BUTTON_RIGHT: 2,
                glfw.MOUSE_BUTTON_MIDDLE: 3
                }

class PseudoMouseEvent:
    """
    This class is a helper class to reuse the events module which is very Vispy oriented
    """
    def __init__(self, pos=(0,0), delta=(0,0), modifiers=None, button=None, buttons=None):
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

def on_close(window):
    pass

def on_mouse_button(window, button, action, mod):
    pos = glfw.get_cursor_pos(window)
    
    if button < 3:
        button = BUTTONMAP.get(button, 0)
    
    # TODO: Check if it is possible to detect multiple mouse button clicks in GLFW and populate buttons accordingly
    # TODO: Implement delta, if needed
    event = PseudoMouseEvent(pos, (0,0), p5.sketch.modifiers, button, [])
    mev = MouseEvent(event, active = (action == glfw.PRESS))
    
    p5.sketch._enqueue_event('mouse_pressed', mev)
    
def on_mouse_scroll(window, x_off, y_off):
    pass

def on_mouse_motion(window, x, y):
    event = PseudoMouseEvent(pos=(x,y), modifiers=p5.sketch.modifiers)
    mev = MouseEvent(event, active = builtins.mouse_is_pressed)

    # Queue a 'mouse_dragged` or `mouse_moved` event, not both similar to p5.js
    p5.sketch._enqueue_event('mouse_dragged' if builtins.mouse_is_pressed else 'mouse_moved' , mev)

def on_key_press(window, key, scancode, action, mod):
    pass
    
def on_key_char(window, text):
    pass