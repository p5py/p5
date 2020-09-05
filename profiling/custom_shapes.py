# Adapted from
import cProfile
import random
from p5 import *

FRAME_MAX = 1000


def setup():
    # Sets the screen to be 720 pixels wide and 400 pixels high
    size(720, 400)


def draw():
    if frame_count >= FRAME_MAX:
        exit()

    def transform(p, a, b): return p * a + b
    # Points adapted from https://github.com/processing/p5.js/issues/3672
    points = np.asarray(((0, 0), (4, 0), (4, 1), (1, 1),
                         (1, 2), (4, 2), (4, 3), (0, 3)))
    shapes_to_draw = 10
    for _ in range(shapes_to_draw):
        with push_matrix():
            begin_shape()
            rotate(random_uniform(0, 2 * PI))
            translate(random.randint(-200, 200), random.randint(-20, 20))
            transformed_pts = transform(
                points, np.asarray(
                    (20, 20)), np.asarray(
                    (width / 2, height / 2)))
            for p in transformed_pts:
                vertex(*p)
            end_shape("CLOSE")


if __name__ == '__main__':
    random.seed(42)
    pr = cProfile.Profile()
    pr.enable()
    try:
        run()
    except BaseException:
        pass
    pr.disable()
    pr.dump_stats("custom_shapes.prof")
