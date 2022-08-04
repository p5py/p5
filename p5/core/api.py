# This file adds Processing API compatibility for p5py

from .structure import push_style, pop_style
from .primitives import rect_mode, ellipse_mode
from .transforms import (
    push_matrix,
    pop_matrix,
    reset_matrix,
    reset_transforms,
    shear_x,
    shear_y,
    rotate_x,
    rotate_y,
    rotate_z,
    apply_matrix,
    print_matrix,
)
from .color import color_mode
from .attribs import no_fill, no_tint, no_stroke, stroke_cap, stroke_join, stroke_weight
from .image import load_image, load_pixels, save_frame, image_mode
from .font import (
    create_font,
    load_font,
    text_font,
    text_size,
    text_width,
    text_descent,
    text_align,
    text_ascent,
    text_leading,
)
from .constants import TESS
from .vertex import (
    begin_shape,
    begin_contour,
    curve_vertex,
    bezier_vertex,
    end_contour,
    end_shape,
    quadratic_vertex,
)
from .material import normal_material, basic_material, blinn_phong_material
from .light import (
    ambient_light,
    directional_light,
    point_light,
    light_falloff,
    light_specular,
)


def push():
    """The push() function saves the current drawing style settings and transformations"""
    push_matrix()
    push_style()


def pop():
    pop_style()
    pop_matrix()


def pushStyle():
    """Save the current style settings and then restores them on exit.

    The 'style' information consists of all the parameters controlled
    by the following functions (the ones indicated by an asterisks '*'
    aren't available yet):

    - background
    - fill, noFill
    - stroke, noStroke
    - rectMode
    - ellipseMode
    - shapeMode
    - colorMode
    - tint
    - (*) strokeWeight
    - (*) strokeCap
    - (*) strokeJoin
    - (*) imageMode
    - (*) textAlign
    - (*) textFont
    - (*) textMode
    - (*) textSize
    - (*) textLeading
    -  emissive
    -  specular
    -  shininess
    -  ambient
    -  material

    """
    push_style()


def popStyle():
    """Restores previously pushed style settings"""
    pop_style()


def rectMode(mode="CORNER"):
    """Change the rect and square drawing mode for the p5.renderer.

    :param mode: The new mode for drawing rects. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CORNER' so calling rect_mode without parameters will reset
        the sketch's rect mode.
    :type mode: str

    """
    rect_mode(mode)


def ellipseMode(mode="CENTER"):
    """Change the ellipse and circle drawing mode for the p5.renderer.

    :param mode: The new mode for drawing ellipses. Should be one of
        {'CORNER', 'CORNERS', 'CENTER', 'RADIUS'}. This defaults to
        'CENTER' so calling ellipse_mode without parameters will reset
        the sketch's ellipse mode.
    :type mode: str

    """
    ellipse_mode(mode)


def pushMatrix():
    """Pushes the current transformation matrix onto the matrix stack."""
    push_matrix()


def popMatrix():
    """Pops the current transformation matrix off the matrix stack."""
    pop_matrix()


def resetTransforms():
    """Reset all transformations to their default state."""
    reset_transforms()


def rotateX(theta):
    """Rotate the view along the x axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    return rotate_x(theta)


def rotateY(theta):
    """Rotate the view along the y axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    return rotate_y(theta)


def rotateZ(theta):
    """Rotate the view along the z axis.

    :param theta: angle by which to rotate (in radians)
    :type theta: float

    :returns: The rotation matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    return rotate_z(theta)


def applyMatrix(transformMatrix):
    """Apply the given matrix to the sketch's transform matrix..

    :param transformMatrix: The new transform matrix.
    :type transformMatrix: np.ndarray (or a 4×4 list)
    """
    apply_matrix(transformMatrix)


def resetMatrix():
    """Reset the current transform matrix."""
    reset_matrix()


def printMatrix():
    """Print the transform matrix being used by the sketch."""
    print_matrix()


def shearX(theta):
    """Shear display along the x-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float

    :returns: The shear matrix used to apply the tranformation.
    :rtype: np.ndarray

    """
    return shear_x(theta)


def shearY(theta):
    """Shear display along the y-axis.

    :param theta: angle to shear by (in radians)
    :type theta: float

    :returns: The shear matrix used to apply the transformation.
    :rtype: np.ndarray

    """
    return shear_y(theta)


def colorMode(mode, max1=255, max2=None, max3=None, maxAlpha=255):
    """Set the color mode of the renderer.

    :param mode: One of {'RGB', 'HSB'} corresponding to Red/Green/Blue
        or Hue/Saturation/Brightness
    :type mode: str

    :param max1: Maximum value for the first color channel (default:
        255)
    :type max1: int

    :param max2: Maximum value for the second color channel (default:
        max1)
    :type max2: int

    :param max3: Maximum value for the third color channel (default:
        max1)
    :type max3: int

    :param maxalpha: Maximum value for the alpha channel (default:
        255)
    :type maxalpha: int

    """
    color_mode(mode, max1, max2, max3, maxAlpha)


def noFill():
    """Disable filling geometry."""
    no_fill()


def strokeWeight(thickness):
    """Sets the width of the stroke used for lines, points, and the border around shapes. All widths are set in units of
     pixels.

    :param weight: thickness of stroke in pixels
    :type weight: int

    """
    stroke_weight(thickness)


def noStroke():
    """Disable drawing the stroke around shapes."""
    no_stroke()


def strokeCap(c):
    """Sets the style of line endings. The ends are SQUARE,
    PROJECT, and ROUND. The default cap is ROUND.

    :param c: either 'SQUARE', 'PROJECT' or 'ROUND'
    :type c: string

    """
    stroke_cap(c)


def strokeJoin(j):
    """Sets the style of the joints which connect line segments.
    These joints are either mitered, beveled, or rounded and
    specified with the corresponding parameters MITER, BEVEL,
    and ROUND. The default joint is MITER.

    :param weight: either 'MITER', 'BEVEL' or 'ROUND'
    :type j: string

    """
    stroke_join(j)


def noTint():
    """Disable tinting of images."""
    no_tint()


def imageMode(mode):
    """Modify the locaton from which the images are drawn.

    Modifies the location from which images are drawn by changing the
    way in which parameters given to :meth:`p5.image` are intepreted.

    The default mode is ``image_mode('corner')``, which interprets the
    second parameter of ``image()`` as the upper-left corner of the
    image. If an additional parameter is specified, it is used to set
    the image's width and height.

    ``image_mode('corners')`` interprets the first parameter of
    ``image()`` as the location of one corner, and the second
    parameter as the opposite corner.

    ``image_mode('center')`` interprets the first parameter of
    ``image()`` as the image's center point. If an additional
    parameter is specified, it is used to set the width and height of
    the image.

    :param mode: should be one of ``{'corner', 'center', 'corners'}``
    :type mode: str

    :raises ValueError: When the given image mode is not understood.
        Check for typoes.

    """
    image_mode(mode)


def loadImage(filename):
    """Load an image from the given filename.

    Loads an image into a variable of type PImage. Four types of
    images may be loaded.

    In most cases, load all images in setup() or outside the draw()
    call to preload them at the start of the program. Loading images
    inside draw() will reduce the speed of a program.

    :param filename: Filename (or path)of the given image. The
        file-extennsion is automatically inferred.
    :type filename: str

    :returns: An :class:`p5.PImage` instance with the given image data
    :rtype: :class:`p5.PImage`

    """
    return load_image(filename)


def loadPixels():
    """Load a snapshot of the display window into the ``pixels`` Image.

    This context manager loads data into the global ``pixels`` Image.
    Once the program execution leaves the context manager, all changes
    to the image are written to the main display.

    """
    load_pixels()


def saveFrame(filename=None):
    save_frame(filename)


def createFont(name, size=10):
    """Create the given font at the appropriate size.

    :param name: Filename of the font file (only pil, otf and ttf
        fonts are supported.)
    :type name: str

    :param size: Font size (only required when `name` refers to a
        truetype font; defaults to None)
    :type size: int | None

    """
    return create_font(name, size)


def loadFont(font_name):
    """Loads the given font into a font object"""
    return load_font(font_name)


def textFont(font, size=10):
    """Set current text font.

    :param font:
    :type font: PIL.ImageFont.ImageFont

    """
    text_font(font, size)


def textAlign(alignX, alignY=None):
    """Set the alignment of drawing text

    :param alignX: "RIGHT", "CENTER" or "LEFT".
    :type alignX: string

    :param alignY: "TOP", "CENTER" or "BOTTOM".
    :type alignY: string

    """
    text_align(alignX, alignY)


def textLeading(leading):
    """Sets the spacing between lines of text in units of pixels

    :param leading: the size in pixels for spacing between lines
    :type align_x: int

    """
    text_leading(leading)


def textSize(size):
    """Sets the current font size

    :param leading: the size of the letters in units of pixels
    :type align_x: int

    """
    text_size(size)


def textWidth(text):
    """Calculates and returns the width of any character or text string

    :param text_string: text
    :type text_string: str

    :returns: width of any character or text string
    :rtype: int

    """
    return text_width(text)


def textAscent():
    """Returns ascent of the current font at its current size

    :returns: ascent of the current font at its current size
    :rtype: float

    """
    return text_ascent()


def textDescent():
    """Returns descent of the current font at its current size

    :returns:  descent of the current font at its current size
    :rtype: float

    """
    return text_descent()


def beginShape(kind=TESS):
    """Begin shape drawing.  This is a helpful way of generating custom shapes quickly.

    :param kind: TESS, POINTS, LINES, TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP, QUADS, or QUAD_STRIP; defaults to TESS
    :type kind: SType
    """
    begin_shape(kind)


def curveVertex(x, y, z=0):
    """
    Specifies vertex coordinates for curves. The first
    and last points in a series of curveVertex() lines
    will be used to guide the beginning and end of a the
    curve. A minimum of four points is required to draw a
    tiny curve between the second and third points. Adding
    a fifth point with curveVertex() will draw the curve
    between the second, third, and fourth points. The
    curveVertex() function is an implementation of
    Catmull-Rom splines.

    :param x: x-coordinate of the vertex
    :type x: float

    :param y: y-coordinate of the vertex
    :type y: float

    :param z: z-coordinate of the vertex
    :type z: float
    """
    curve_vertex(x, y, z)


def bezierVertex(x2, y2, x3, y3, x4, y4):
    """
    Specifies vertex coordinates for Bezier curves

    :param x2: x-coordinate of the first control point
    :type x2: float

    :param y2: y-coordinate of the first control point
    :type y2: float

    :param x3: x-coordinate of the second control point
    :type x3: float

    :param y3: y-coordinate of the second control point
    :type y3: float

    :param x4: x-coordinate of the anchor point
    :type x4: float

    :param y4: y-coordinate of the anchor point
    :type y4: float
    """
    bezier_vertex(x2, y2, x3, y3, x4, y4)


def quadraticVertex(cx, cy, x3, y3):
    """
    Specifies vertex coordinates for quadratic Bezier curves

    :param cx: x-coordinate of the control point
    :type cx: float

    :param cy: y-coordinate of the control point
    :type cy: float

    :param x3: x-coordinate of the anchor point
    :type x3: float

    :param y3: y-coordinate of the anchor point
    :type y3: float

    """
    quadratic_vertex(cx, cy, x3, y3)


def beginContour():
    """
    Use the beginContour() and endContour() functions
    to create negative shapes within shapes such as
    the center of the letter 'O'. beginContour() begins
    recording vertices for the shape and endContour() stops
    recording. The vertices that define a negative shape must
    "wind" in the opposite direction from the exterior shape.
    First draw vertices for the exterior clockwise order, then
    for internal shapes, draw vertices shape in counter-clockwise.

    """
    begin_contour()


def endContour():
    """Ends the current contour.

    For more info, see :any:`begin_contour`.
    """
    end_contour()


def endShape(mode=""):
    """
    The endShape() function is the companion to beginShape()
    and may only be called after beginShape(). When endshape()
    is called, all of image data defined since the previous call
    to beginShape() is rendered.

    :param mode: use CLOSE to close the shape
    :type mode: str

    """
    return end_shape(mode)


def normalMaterial():
    """The color is determined by the normal vector of a surface. Does not respond to lights.

    Useful for debugging.
    """
    normal_material()


def basicMaterial(r, g, b):
    """The default material. Always displays a solid color.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    basic_material(r, g, b)


def blinnPhongMaterial():
    """Material based on the Blinn-Phong reflection model. This is the most "realistic" material in p5py.

    Blinn-Phong shading can be decomposed into three parts:
    ambient, diffuse, and specular.

    The ambient component is essentially a constant term that is alway present.
    We calculate it by summing all the ambient lights in a scene and multiplying it
    with the normalized ambient coefficent set by ambient.

    The diffuse component takes the normal vector of a surface into account and
    varies how much light is reflected depending on the angle that the surface
    makes with the incoming light.

    The specular component not only accounts for the direction of the light
    (like the diffuse component) but also the direction of the viewer. If the
    viewer is not on the path of the reflected light, the specular component
    falls off quickly, producing the glossy reflections we see on some materials.

    The color shown on the user's screen is the sum of all three components.
    """
    blinn_phong_material()


def ambientLight(r, g, b):
    """Adds an ambient light.

    Ambient light comes from all directions towards all directions.
    Ambient lights are almost always used in combination with other types of lights.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    ambient_light(r, g, b)


def directionalLight(r, g, b, x, y, z):
    """Adds a directional light.
    Directional light comes from one direction: it is stronger when hitting a surface squarely,
    and weaker if it hits at a gentle angle.
    After hitting a surface, directional light scatters in all directions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float

    :param x: x component of the direction vector
    :type x: float

    :param y: y component of the direction vector
    :type y: float

    :param z: z component of the direction vector
    :type z: float
    """
    directional_light(r, g, b, x, y, z)


def pointLight(r, g, b, x, y, z):
    """Adds a point light.
    Point light comes from one location and emits to all directions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float

    :param x: x component of the location vector
    :type x: float

    :param y: y component of the location vector
    :type y: float

    :param z: z component of the location vector
    :type z: float
    """
    point_light(r, g, b, x, y, z)


def lightFalloff(constant, linear, quadratic):
    """Sets the falloff rates for point lights. Affects only the elements which are created after it in the code.

    d = distance from light position to vertex position

    falloff = 1 / (constant + d * linear + (d*d) * quadratic)

    If the coefficient is 0, then that term is ignored.
    The P3D renderer defaults to (0, 0, 0), i.e. no falloff.

    :param constant: coefficient for the constant term
    :type constant: float

    :param linear: coefficient for the linear term
    :type linear: float

    :param quadratic: coefficient for the quadratic term
    :type quadratic: float
    """
    light_falloff(constant, linear, quadratic)


def lightSpecular(r, g, b):
    """Sets the specular color for lights. Only visible with :any:`p5.blinn_phong_material`. Is set to (0 ,0, 0)
     by default.
    Affects only the elements which are created after it in the code.

    Specular refers to light which bounces off a surface in a preferred direction
    (rather than bouncing in all directions like a diffuse light) and is used for
    creating highlights. The specular quality of a light interacts with the specular
    material qualities set through the `specular()` and `shininess()` functions.

    :param r: red channel
    :type r: float

    :param g: green channel
    :type g: float

    :param b: blue channel
    :type b: float
    """
    light_specular(r, g, b)
