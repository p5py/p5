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

from PIL import Image
import numpy as np
import vispy
from vispy import app
from vispy import gloo
from vispy import io

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

def _transform_vertices(vertices, local_matrix, global_matrix):
    return np.dot(np.dot(vertices, local_matrix.T), global_matrix.T)[:, :3]

def render(shape):
    vertices = shape._draw_vertices
    n, _ = vertices.shape
    tverts = _transform_vertices(
        np.hstack([vertices, np.zeros((n, 1)), np.ones((n, 1))]),
        shape._matrix,
        renderer.transform_matrix)
    fill = shape.fill.normalized if shape.fill else None
    stroke = shape.stroke.normalized if shape.stroke else None

    edges = shape._draw_edges
    faces = shape._draw_faces

    if edges is None:
        print(vertices)
        print("whale")
        exit()

    if 'open' in shape.attribs:
        overtices = shape._draw_outline_vertices
        no, _  = overtices.shape
        toverts = _transform_vertices(
            np.hstack([overtices, np.zeros((no, 1)), np.ones((no, 1))]),
            shape._matrix,
            renderer.transform_matrix)

        add_to_draw_queue('path', toverts, shape._draw_outline_edges,
                          None, None, stroke)
        add_to_draw_queue('poly', tverts, edges, faces, fill, None)
    else:
        add_to_draw_queue(shape.kind, tverts, edges, faces, fill, stroke)


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

        self._save_fname = 'screen'
        self._save_fname_num = 0
        self._save_flag = False

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
                    self.looping = False
                else:
                    self.draw_method()
                    self.redraw = False

            while len(self.handler_queue) != 0:
                function, event = self.handler_queue.pop(0)
                event._update_builtins()
                function(event)

        if self._save_flag:
            self._save_buffer()
        self.update()

    def _save_buffer(self):
        """Save the renderer buffer to the given file.
        """
        img_data = renderer.fbuffer.read(mode='color', alpha=False)
        img = Image.fromarray(img_data)
        img.save(self._save_fname)
        self._save_flag = False

    def screenshot(self, filename):
        self.queue_screenshot(filename)
        renderer.flush_geometry()
        self._save_buffer()

    def queue_screenshot(self, filename):
        """Save the current frame
        """
        fname_split = filename.split('.')
        ext = '.' + fname_split[-1]
        stem = '.'.join(fname_split[:-1])
        self._save_fname = stem + str(self._save_fname_num).zfill(4) + ext
        self._save_fname_num = self._save_fname_num + 1
        self._save_flag = True

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
