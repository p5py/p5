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

import builtins
from functools import wraps
import time

import vispy
from vispy import app

from .events import KeyEvent
from .events import MouseEvent
from .events import handler_names


def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing.
    """
    pass


# import pyglet
# pyglet.options["shadow_window"] = False

# __all__ = ['setup', 'draw', 'run', 'no_loop', 'loop', 'redraw', 'size',
#            'title', 'no_cursor', 'cursor', 'exit',]

# builtins.width = 360
# builtins.height = 360
# builtins.title = "p5"

# builtins.frame_count = -1
# builtins.frame_rate = 30

# last_recorded_time = time.time()

# builtins.pixel_width = 1
# builtins.pixel_height = 1

# display = pyglet.canvas.get_display()
# screen = display.get_default_screen()
# template = pyglet.gl.Config(double_buffer=1, sample_buffers=1)
# config = screen.get_best_config(template)

# window = pyglet.window.Window(
#     width=builtins.width,
#     height=builtins.height,
#     caption=builtins.title,
#     resizable=False,
#     visible=False,
#     vsync=False,
#     config=config,
# )

# def _window_setup():
#     global window
#     actual_width, actual_height = window.get_viewport_size()
#     builtins.pixel_x_density = actual_width / builtins.width
#     builtins.pixel_y_density = actual_height / builtins.height

#     window.set_minimum_size(100, 100)

# # DO NOT REMOVE THIS
# #
# # We tried removing this line and things broke badly on Mac machines.
# # We still don't know why. Let's just keep this here for now.
# _ = pyglet.clock.ClockDisplay()

# def _dummy_handler(*args, **kwargs):
#     return pyglet.event.EVENT_HANDLED

# handler_names = [ 'key_press', 'key_pressed', 'key_released',
#                   'key_typed', 'mouse_clicked', 'mouse_dragged',
#                   'mouse_moved', 'mouse_pressed', 'mouse_released',
#                   'mouse_wheel',]

# handlers =  dict.fromkeys(handler_names, _dummy_handler)

# handler_queue = []

# looping = True
# redraw = False
# setup_done = False

# def draw():
#     """Continuously execute code defined inside.

#     The `draw()` function is called directly after `setup()` and all
#     code inside is continuously executed until the program is stopped
#     (using `exit()`) or `no_loop()` is called.

#     """
#     pass

# def setup():
#     """Called to setup initial sketch options.

#     The `setup()` function is run once when the program starts and is
#     used to define initial environment options for the sketch.

#     """
#     pass

# def update(dt):
#     global handler_queue
#     global redraw
#     global setup_done
#     global last_recorded_time

#     with renderer.draw_loop():
#         if looping or redraw:
#             builtins.frame_count += 1
#             now = time.time()
#             builtins.frame_rate = 1 / (now - last_recorded_time)
#             last_recorded_time = now
#             if not setup_done:
#                 setup()
#                 setup_done = True
#                 if not window.visible:
#                     window.set_visible(True)
#             else:
#                 draw()
#                 redraw = False
#         for function, event in handler_queue:
#             function(event)
#         handler_queue = []

# def fix_handler_interface(func):
#     """Make sure that `func` takes at least one argument as input.

#     :returns: a new function that accepts arguments.
#     :rtype: func
#     """
#     @wraps(func)
#     def fixed_func(*args, **kwargs):
#         return_value = func()
#         return return_value

#     if func.__code__.co_argcount == 0:
#         return fixed_func
#     else:
#         return func

# def run(sketch_setup=None, sketch_draw=None, frame_rate=60):
#     """Run a sketch.

#     if no `sketch_setup` and `sketch_draw` are specified, p5 automatically
#     "finds" the user-defined setup and draw functions.

#     :param sketch_setup: The setup function of the sketch (None by
#          default.)
#     :type sketch_setup: function

#     :param sketch_draw: The draw function of the sketch (None by
#         default.)
#     :type sketch_draw: function

#     :param frame_rate: The target frame rate for the sketch.
#     :type frame_rate: int :math:`\geq 1`

#     """
#     global draw
#     global setup

#     _window_setup()

#     if sketch_setup is not None:
#         setup = sketch_setup
#     elif hasattr(__main__, 'setup'):
#         setup = __main__.setup

#     if sketch_draw is not None:
#         draw = sketch_draw
#     elif hasattr(__main__, 'draw'):
#         draw = __main__.draw

#     for handler in handler_names:
#         if hasattr(__main__, handler):
#             handler_func = getattr(__main__, handler)
#             handlers[handler] = fix_handler_interface(handler_func)

#     renderer.initialize(window.context)
#     pyglet.clock.schedule_interval(update, 1 / max(frame_rate, 1))
#     pyglet.app.run()


# def draw_shape(shape):
#     """Handle the lower level stuff associated with drawing a shape.

#     :param shape: The shape to be drawn.
#     :type shape: Shape

#     """
#     # TODO (abhikpal 2017-08-05)
#     #
#     # Add a check that insures that we don't call the renderer
#     # directly while drawing a shape.
#     renderer.render(shape)

def draw_shape(*args, **kwargs):
    pass

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
        self.measure_fps(callback=lambda _: None)
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

        builtins.frame_rate = round(self.fps, 2)

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

        # reinit renderer()
        # clear
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
