#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
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

from PIL import Image
from vispy import app

from p5.core import p5

from ..events import KeyEvent
from ..events import MouseEvent
from ..events import handler_names


def _dummy(*args, **kwargs):
    """Eat all arguments, do nothing."""
    pass


class VispySketch(app.Canvas):
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

    def __init__(self, setup_method, draw_method, handlers=dict(), frame_rate=60):
        app.Canvas.__init__(
            self,
            title=builtins.title,
            size=(builtins.width, builtins.height),
            keys="interactive",
            resizable=True,
        )

        self.events.ignore_callback_errors = False
        self.setup_method = setup_method
        self.draw_method = draw_method

        self.exiting = False
        self.looping = None
        self.redraw = None
        self.setup_done = False
        self.timer = app.Timer(1.0 / frame_rate, connect=self.on_timer)
        self.timer.events.ignore_callback_errors = False

        self.handlers = dict()
        for handler_name in handler_names:
            self.handlers[handler_name] = handlers.get(handler_name, _dummy)

        self.handler_queue = []

        self._save_fname = "screen"
        self._save_flag = False

        builtins.frame_count = -1

        p5.renderer.reset_view()
        p5.renderer.clear()

    def on_timer(self, event):
        self.measure_fps(callback=lambda _: None)
        builtins.frame_rate = round(self.fps, 2)

        with p5.renderer.draw_loop():
            if not self.setup_done:
                builtins.frame_count += 1
                self.setup_method()
                self.setup_done = True
                self.show(visible=True)
                if self.redraw is None:
                    self.redraw = False
                if self.looping is None:
                    self.looping = True

            elif self.redraw:
                builtins.frame_count += 1
                self.draw_method()
                self.redraw = False
            elif self.looping:
                builtins.frame_count += 1
                self.draw_method()
                self.redraw = False
            elif not self.looping:
                pass

            while len(self.handler_queue) != 0:
                function, event = self.handler_queue.pop(0)
                event._update_builtins()
                function(event)

        if self._save_flag:
            self._save_buffer()
        self.update()

        if self.exiting:
            self.close()
            return

    def _save_buffer(self):
        """Save the renderer buffer to the given file."""
        img_data = p5.renderer.fbuffer.read(mode="color", alpha=False)
        img = Image.fromarray(img_data)
        img.save(self._save_fname)
        self._save_flag = False

    def screenshot(self, filename):
        self.queue_screenshot(filename)
        p5.renderer.flush_geometry()
        self._save_buffer()

    def queue_screenshot(self, filename):
        """Save the current frame"""
        self._save_fname = filename
        self._save_flag = True

    def on_close(self, event):
        self.timer.stop()
        app.quit()

    def on_draw(self, event):
        pass

    def on_resize(self, event):
        builtins.width = int(self.size[0])
        builtins.height = int(self.size[1])

        p5.renderer.reset_view()
        with p5.renderer.draw_loop():
            p5.renderer.clear()

    def _enqueue_event(self, handler_name, event):
        event._update_builtins()
        self.handler_queue.append((self.handlers[handler_name], event))

    def on_key_press(self, event):
        kev = KeyEvent(event, active=True)
        self._enqueue_event("key_pressed", kev)

    def on_key_release(self, event):
        kev = KeyEvent(event)
        self._enqueue_event("key_released", kev)
        if not (event.text == ""):
            self._enqueue_event("key_typed", kev)

    def on_mouse_press(self, event):
        mev = MouseEvent(event, active=True)
        self._enqueue_event("mouse_pressed", mev)

    def on_mouse_double_click(self, event):
        mev = MouseEvent(event)
        self._enqueue_event("mouse_double_clicked", mev)

    def on_mouse_release(self, event):
        mev = MouseEvent(event)
        self._enqueue_event("mouse_released", mev)
        self._enqueue_event("mouse_clicked", mev)

    def on_mouse_move(self, event):
        mev = MouseEvent(event, active=builtins.mouse_is_pressed)
        self._enqueue_event("mouse_moved", mev)
        if builtins.mouse_is_pressed:
            self._enqueue_event("mouse_dragged", mev)

    def on_mouse_wheel(self, event):
        mev = MouseEvent(event, active=builtins.mouse_is_pressed)
        self._enqueue_event("mouse_wheel", mev)

    # def on_touch(self, event):
    #     self._enqueue_event('touch', event)

    # def on_stylus(self, event):
    #     self._enqueue_event('stylus', event)

    def exit(self):
        self.exiting = True
