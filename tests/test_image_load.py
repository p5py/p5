import sys
import unittest
import threading
import types
import time
from time import perf_counter as pc

sys.path.append('../')
from p5 import *

from p5 import PImage, font, renderer
from vispy.gloo import Program

# def assertRuntime(milliseconds):
#     def inner(func):
#         def wrapper(self, *args, **kwargs):
#             start = pc()
#             func(self, *args, **kwargs)
#             elapsed = int((pc() - start) * 1000)
#             assert elapsed < milliseconds, f"{func.__name__} runtime exceeds {milliseconds} milliseconds. Took {elapsed}."
#         return wrapper
#     return inner
#
#
# class TestImageLoad(unittest.TestCase):
#
#     @assertRuntime(1000)
#     def test_image_load(self):
#         try:
#             run()
#         except:
#             print("shutting down")
#         text("hello", (5,5))
#         self.assertTrue(True)

def timer(func):
    def inner(limit=None):
        def wrapper(*args, **kwargs):
            start = pc()
            func(*args, **kwargs)
            elapsed = int((pc() - start) * 1000)

            if limit and elapsed > limit:
                print(f"{frame_count}: WARN: {func.__name__}() exceeds {limit} ms. Took {elapsed} ms.")
            else:
                print(f"{frame_count}: {func.__name__}: {elapsed} ms.")
        return wrapper
    return inner

text = timer(text)()
font.image = timer(font.image)()

def hello():
    print("hello")

setattr(PImage, "_load", timer(PImage._load)())
renderer.render_image = timer(renderer.render_image)()
setattr(Program, "draw", timer(Program.draw)())


def setup():
    size(640, 480)

def draw():
    background(255)
    ellipse((50, 50), 100, 100)
    text("hello", (50, 50))
    no_loop()
    exit()

run()
