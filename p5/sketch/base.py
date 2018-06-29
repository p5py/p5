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
import time

import vispy
from vispy import app
from vispy import gloo

from .events import KeyEvent
from .events import MouseEvent
from .events import handler_names
from .render import Renderer

# Instead of exposing the renderer direcly, we set up the
# sketch a "proxy". Whenever an attribute name occurs in the
# list below, attribute access is delegated to the renderer.
_proxy_attribs = [ 'fill_enabled', 'fill_color',
                         'stroke_enabled', 'stroke_color',
                         'background_color', 'modelview',
                         'projection', 'transform', ]



class Sketch(app.Canvas):
    """The main sketch instance.

    :param setup: Setup method for the sketch. This is run
        exactly once for each run of the sketch.
    :type setup: function

    :param draw: Draw method for the sketch which keeps running
        indefinitely.
    :type draw: function

    :param handlers: Dictionary containing the event handlers for the
        sketch. An empty dict by default.
    :type handlers: { str: function }

    :param frame_rate: Frame rate for the sketch.
    :type frame_rate: int

    """
    def __init__(self, setup, draw, handlers=dict(), frame_rate=60):
        app.Canvas.__init__(
            self,
            title=builtins.title,
            size=(builtins.width, builtins.height),
            keys='interactive',
            resizable=False,
        )

        self.setup_method = setup
        self.draw_method = draw

        self.looping = True
        self.redraw = False
        self.setup_done = False
        self.timer = app.Timer(1.0 / frame_rate, connect=self.on_timer)

        def _dummy(*args, **kwargs): pass
        self.handlers = dict()
        for handler_name in handler_names:
            self.handlers[handler_name] = handlers.get(handler_name, _dummy)

        self.handler_queue = []

        px, py = self.physical_size
        sx, sy = self.size

        self.renderer = Renderer(self.size, (px // sx, py // sy))
        self.renderer.clear()

    def __getattr__(self, name):
        if name in _proxy_attribs:
            return getattr(self.renderer, name)
        err = "'{}' object has no attribute '{}'"
        raise AttributeError(err.format('Foo', name))

    def __setattr__(self, name, value):
        if name in _proxy_attribs:
            setattr(self.renderer, name, value)
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in _proxy_attribs:
            delattr(self.renderer, name)
        else:
            super().__delattr__(name)

    def draw_shape(self, shape):
        """Handle the lower level stuff associated with drawing a shape.
        
        :param shape: The shape to be drawn.
        :type shape: Shape

        """
        return self.renderer.add_to_queue(shape)

    def on_timer(self, event):
        self.measure_fps(callback=lambda _: None)
        builtins.frame_rate = round(self.fps, 2)
        with self.renderer:
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
        self.renderer.size = (builtins.width, builtins.height)

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
        mev = MouseEvent(event)
        self._enqueue_event('mouse_moved', mev)
        if builtins.mouse_is_pressed:
            self._enqueue_event('mouse_dragged', mev)

    def on_mouse_wheel(self, event):
        mev = MouseEvent(event)
        self._enqueue_event('mouse_wheel', mev)

    # def on_touch(self, event):
    #     self._enqueue_event('touch', event)

    # def on_stylus(self, event):
    #     self._enqueue_event('stylus', event)
