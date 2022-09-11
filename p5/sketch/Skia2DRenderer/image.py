from p5.core import constants
from p5.core import PImage
import numpy as np
import skia
import builtins


class SkiaPImage(PImage):
    def __init__(self, width, height, pixels=None):
        self._width = width
        self._height = height
        self.pixels = (
            pixels
            if pixels is not None
            else np.zeros((width, height, constants.RGBA_CHANNELS), dtype=np.uint8)
        )

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, size):
        self.width, self.height = size
        self.pixels.resize((*size, constants.RGBA_CHANNELS))

    @property
    def aspect_ratio(self):
        return self.width / self.height

    def load_pixels(self):
        builtins.pixels = self.pixels

    def update_pixels(self):
        pass

    def mask(self, image):
        """
        :param image: Image to be used as make
        :type image: SkiaPImage
        """
        with skia.Surface(self.pixels) as canvas:
            canvas.drawImage(image.get_skia_image())

    def filter(self, kind, param=0.5):
        # https://www.baeldung.com/cs/convert-rgb-to-grayscale#3-luminosity-method
        if kind == constants.THRESHOLD:
            threshold = param * 255
            mask = np.dot(self.pixels[..., :3], [0.2989, 0.5870, 0.1140]) < threshold
            self.pixels[:, :, :3][mask] = 1

        if kind == constants.GRAY:
            mask = np.dot(self.pixels[..., :3], [0.2989, 0.5870, 0.1140])
            mask = np.array([[i] * 3 for i in mask.flatten()]).reshape(
                (self.pixels.shape[0], self.pixels.shape[1], 3)
            )
            self.pixels[:, :, :3] = mask

        if kind == constants.OPAQUE:
            self.pixels[..., 3:] = 255

        if kind == constants.INVERT:

            def invert(x):
                return 255 - x

            self.pixels[..., :3] = invert(self.pixels[..., :3])

        if kind == constants.POSTERIZE:
            raise NotImplementedError("POSTERIZE is not yet implemented for skia")

        if kind == constants.DILATE:
            with skia.Surface(self.pixels) as canvas:
                paint = skia.Paint(ImageFilter=skia.ImageFilters.Dilate(param, param))
                image = canvas.getSurface().makeImageSnapshot()
                canvas.clear(skia.ColorWHITE)
                canvas.drawImage(image, 0, 0, paint)

        if kind == constants.ERODE:
            with skia.Surface(self.pixels) as canvas:
                paint = skia.Paint(ImageFilter=skia.ImageFilters.Erode(param, param))
                image = canvas.getSurface().makeImageSnapshot()
                canvas.clear(skia.Color(0, 0, 0, 0))
                canvas.drawImage(image, 0, 0, paint)

        if kind == constants.BLUR:
            with skia.Surface(self.pixels) as canvas:
                paint = skia.Paint(ImageFilter=skia.ImageFilters.Blur(param, param))
                image = canvas.getSurface().makeImageSnapshot()
                canvas.clear(skia.Color(0, 0, 0, 0))
                canvas.drawImage(image, 0, 0, paint)

    def blend(self, other, mode):
        # TODO: Implement blend
        raise NotImplementedError("To be implemented")

    def save(self, filename):
        if filename.endswith(".png"):
            skia.Image.fromarray(self.pixels).save(filename, skia.kPNG)
        else:
            skia.Image.fromarray(self.pixels).save(filename, skia.kJPEG)

    def get_skia_image(self):
        return skia.Image.fromarray(self.pixels)
