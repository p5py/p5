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
from vispy import gloo

from .events import KeyEvent
from .events import MouseEvent
from .events import handler_names

from .renderer import draw_loop
from .renderer import initialize_renderer
from .renderer import clear
from .renderer import reset_view
from .renderer import render

def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing.
    """
    pass

def draw_shape(shape):
    """Handle the lower level stuff associated with drawing a shape.

    :param shape: The shape to be drawn.
    :type shape: Shape

    """
    # TODO (abhikpal 2017-08-05)
    #
    # Add a check that insures that we don't call the renderer
    # directly while drawing a shape.
    render(shape)

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

        initialize_renderer()
        clear()

    def on_timer(self, event):
        self.measure_fps(callback=lambda _: None)
        builtins.frame_rate = round(self.fps, 2)
        with draw_loop():
            if self.looping or self.redraw:
                builtins.frame_count += 1
                if not self.setup_done:
                    self.setup_method()
                    self.setup_done = True
                    self.show(visible=True)
                else:
                    self.draw_method()
                    self.redraw = False

            # TODO: restore the previous state of builtins after dealing
            # with all the handlers.
            while len(self.handler_queue) != 0:
                function, event = self.handler_queue.pop(0)
                event._update_builtins()
                function(event)
        self.update()

    def on_close(self, event):
        exit()

    def on_draw(self, event):
        pass

    def on_resize(self, event):
        # we want programmers to be able to resize windows (using the
        # size() method), however, all user attempts to resize the
        # window should be ignored.

        # reinit renderer()
        reset_view()
        clear()
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
