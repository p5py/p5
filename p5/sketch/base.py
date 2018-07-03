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

import numpy as np
import vispy
from vispy import app
from vispy import gloo

from .. sketch import renderer

from .events import KeyEvent
from .events import MouseEvent
from .events import handler_names

from .renderer import draw_loop
from .renderer import initialize_renderer
from .renderer import clear
from .renderer import reset_view
from .renderer import add_to_draw_queue

def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing.
    """
    pass

def draw_shape(shape):
    """Handle the lower level stuff associated with drawing a shape.

    :param shape: The shape to be drawn.
    :type shape: Shape

    """
    num_shape_verts = len(shape.vertices)

    if shape.kind.lower() == 'point':
        idx = np.arange(0, num_shape_verts, dtype=np.uint32)
    elif shape.kind.lower() == 'line':
        idx = np.array(shape.edges, dtype=np.uint32).ravel()
    else:
        idx = np.array(shape.faces, dtype=np.uint32).ravel()

    shape.transform(renderer.transform_matrix)
    vertices = shape.transformed_vertices[:, :3]

    add_to_draw_queue(shape.kind.lower(), vertices, shape.edges, shape.faces,
                      renderer.fill_color, renderer.stroke_color)

def draw_pshape(shape):
    vertices = shape.apply_matrix(renderer.transform_matrix)
    add_to_draw_queue('poly', vertices, shape._tri.edges,
                      shape._tri.tris, renderer.fill_color,
                      renderer.stroke_color)

class Sketch(app.Canvas):
    """The main sketch instance.

    :param setup_method: Setup method for the sketch. This is run
        exactly once for each run of the sketch.
    :type setup_method: function

    :param draw_method: Draw method for the sketch which keeps running
        indefinitely.
    :type draw_method: function

    :param handlers: Dictionary containing the event handlers for the
        sketch. By default, maps to an empty dict.
        nothing.
    :type handlers: { str: function }

    :param frame_rate:
    :type frame_rate: int

    """
    def __init__(self, setup_method, draw_method,
                 handlers=dict(), frame_rate=60):
        app.Canvas.__init__(
            self,
            title=builtins.title,
            size=(builtins.width, builtins.height),
            keys='interactive',
            resizable=False,
        )

        self.setup_method = setup_method
        self.draw_method = draw_method

        self.looping = True
        self.redraw = False
        self.setup_done = False
        self.timer = app.Timer(1.0 / frame_rate, connect=self.on_timer)

        self.handlers = dict()
        for handler_name in handler_names:
            self.handlers[handler_name] = handlers.get(handler_name, _dummy)

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
                    self.redraw = True
                else:
                    self.draw_method()
                    self.redraw = False

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
        reset_view()
        with draw_loop():
            clear()

    def _enqueue_event(self, handler_name, event):
        event._update_builtins()
        self.handler_queue.append((self.handlers[handler_name], event))

    def on_key_press(self, event):
        kev = KeyEvent(event, active=True)
        self._enqueue_event('key_pressed', kev)

    def on_key_release(self, event):
        kev = KeyEvent(event)
        self._enqueue_event('key_released', kev)
        if not (event.text is ''):
            self._enqueue_event('key_typed', kev)

    def on_mouse_press(self, event):
        mev = MouseEvent(event, active=True)
        self._enqueue_event('mouse_pressed', mev)

    def on_mouse_double_click(self, event):
        mev = MouseEvent(event)
        self._enqueue_event('mouse_double_clicked', mev)

    def on_mouse_release(self, event):
        mev = MouseEvent(event)
        self._enqueue_event('mouse_released', mev)
        self._enqueue_event('mouse_clicked', mev)

    def on_mouse_move(self, event):
        mev = MouseEvent(event, active=builtins.mouse_is_pressed)
        self._enqueue_event('mouse_moved', mev)
        if builtins.mouse_is_pressed:
            self._enqueue_event('mouse_dragged', mev)

    def on_mouse_wheel(self, event):
        mev = MouseEvent(event, active=builtins.mouse_is_pressed)
        self._enqueue_event('mouse_wheel', mev)

    # def on_touch(self, event):
    #     self._enqueue_event('touch', event)

    # def on_stylus(self, event):
    #     self._enqueue_event('stylus', event)
