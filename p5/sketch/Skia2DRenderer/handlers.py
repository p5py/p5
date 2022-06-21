
"""
This file contains the handlers needed for glfw event handling
"""


import builtins
import glfw
from p5.core import p5
from p5.sketch.events import MouseEvent

from dataclasses import dataclass
from time import time


BUTTONMAP = {glfw.MOUSE_BUTTON_LEFT: 1,
                glfw.MOUSE_BUTTON_RIGHT: 2,
                glfw.MOUSE_BUTTON_MIDDLE: 3
                }

@dataclass
class InputState:
    """
    A class to store the current state of Input
    """
    modifiers: list
    last_mouse_clicked_time: float
    

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

# Hold the input state for current sketch
input_state = InputState([], 0)
    


def on_mouse_button(window, button, action, mod):
    pos = glfw.get_cursor_pos(window)
    
    if button < 3:
        button = BUTTONMAP.get(button, 0)
    
    # TODO: Check if it is possible to detect multiple mouse button clicks in GLFW and populate buttons accordingly
    # TODO: Implement delta, if needed
    event = PseudoMouseEvent(pos, (0,0), input_state.modifiers, button, [])
    mev = MouseEvent(event, active = (action == glfw.PRESS))

    if action == glfw.PRESS:
        p5.sketch._enqueue_event('mouse_pressed', mev)
    else:
        p5.sketch._enqueue_event('mouse_released', mev)
        p5.sketch._enqueue_event('mouse_clicked', mev)
        
        dt_max = 0.3  # time in seconds for a double-click detection
        if time() - input_state.last_mouse_clicked_time <= dt_max:
            p5.sketch._enqueue_event('mouse_double_clicked', mev)

        input_state.last_mouse_clicked_time = time()
        
def on_mouse_scroll(window, x_off, y_off):
    pass

def on_mouse_motion(window, x, y):
    event = PseudoMouseEvent(pos=(x,y), modifiers=input_state.modifiers)
    mev = MouseEvent(event, active = builtins.mouse_is_pressed)

    # Queue a 'mouse_dragged` or `mouse_moved` event, not both similar to p5.js
    p5.sketch._enqueue_event('mouse_dragged' if builtins.mouse_is_pressed else 'mouse_moved' , mev)

def on_key_press(window, key, scancode, action, mod):
    pass
    
def on_key_char(window, text):
    pass

def on_close(window):
    pass