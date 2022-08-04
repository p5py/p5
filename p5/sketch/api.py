# This file adds compatibility for processing API

from .userspace import no_loop, save_frame


def noLoop():
    """Stop draw() from being continuously called.

    By default, the sketch continuously calls `draw()` as long as it
    runs. Calling `noLoop()` stops draw() from being called the next
    time. Note that this only prevents execution of the code inside
    `draw()` and the user can manipulate the screen contents through
    event handlers like `mousePressed()`, etc.

    """
    no_loop()


def saveFrame():
    """Save a numbered sequence of images whenever the function is run.

    Saves a numbered sequence of images, one image each time the
    function is run. To save an image that is identical to the display
    window, run the function at the end of :meth:`p5.draw` or within
    mouse and key events such as :meth:`p5.mouse_pressed` and
    :meth:`p5.key_pressed`.

    If saveFrame() is used without parameters, it will save files as
    screen-0000.png, screen-0001.png, and so on. Append a file
    extension, to indicate the file format to be used. Image files are
    saved to the sketch's folder. Alternatively, the files can be
    saved to any location on the computer by using an absolute path
    (something that starts with / on Unix and Linux, or a drive letter
    on Windows).

    :param filename: name (or name with path) of the image file.
        (defaults to ``screen.png``)

    :type filename: str

    """
    save_frame()
