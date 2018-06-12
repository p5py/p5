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

# import __main__
# import builtins

# from vispy import app

# app.use(backend='PyQt5')

# # the global sketch instance.
# current_sketch = None

# class Sketch(app.Canvas):
#     def __init__(self, *args, **kwargs):
#         app.Canvas.__init__(self, *args, **kwargs)

#     def on_draw(self):
#         pass


# def exit(*args, **kwargs):
#     """Exit the sketch.

#     `exit()` overrides Python's builtin exit() function and makes sure
#     that necessary cleanup steps are performed before exiting the
#     sketch.

#     :param args: positional argumets to pass to Python's builtin
#         `exit()` function.

#     :param kwargs: keyword-arguments to pass to Python's builtin
#         `exit()` function.
#     """
#     app.quit()
#     builtins.exit(*args, **kwargs)

# def run():
#     global current_sketch
#     current_sketch = Sketch(
#         title=builtins.title,
#         size=(builtins.width, builtins.height),
#         resizeable=False,
#         keys='interactive',
#     )
#     current_sketch.show()
#     app.run()
