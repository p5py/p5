import builtins

"""
This file contains the handlers needed for glfw event handling
"""

# TODO : Make a raw_event class and populate it with data about current events
# TODO : Design of raw_event should follow that of Vispy's raw event beacuse events.py is highly based on it  

def mouse_callback_handler(window, xpos, ypos):
    builtins.mouse_x = xpos
    builtins.mouse_y = ypos
    
    
    
    