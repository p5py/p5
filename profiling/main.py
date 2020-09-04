import importlib
import time
import cProfile
import p5

filenames = [
    'arcs',
    'custom_shapes',
    'triangle_strip',
    'custom_shapes2',
    'curves',
    'primitives']
max_frames = 100
e = SystemExit()

for name in filenames:
    p5 = importlib.import_module('p5')
    module = importlib.import_module(name)
    curr_frames = 0

    def draw():
        global curr_frames
        curr_frames += 1
        if curr_frames > max_frames:
            p5.exit()
        module.draw()

    pr = cProfile.Profile()
    pr.enable()
    start_time = time.process_time()
    try:
        p5.run(sketch_draw=draw, sketch_setup=module.setup)
    except BaseException as curr_e:
        elapsed_time = time.process_time() - start_time
        print(
            "{0} took {1} seconds to render {2} frames".format(
                name,
                elapsed_time,
                max_frames))
        e = curr_e
    pr.disable()
    pr.dump_stats(name + ".prof")

raise e
