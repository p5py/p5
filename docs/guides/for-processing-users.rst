=======================
p5 for Processing users
=======================

p5 API borrows many core ideas from the Processing so most of the API
looks similar. This document lists the major differences between
Processing and the p5 API.

In addition to skimming through this document, you should also check
the API reference for more details and take a look at complete working
examples on the `examples repository
<https://github.com/p5py/p5-examples>`_.

Naming conventions
==================

* Most function names are now in
  :code:`lowercase_separated_by_underscores` as opposed to the
  :code:`lowerCamelCase` in Processing. So, if a method was called
  :code:`bezierPoint` in Processing it will be called
  :code:`bezier_point` in p5.

* Mathematical constants like :math:`\pi` are still in
  :code:`UPPPERCASE_SEPARATED_BY_UNDERSCORES`. Note that :code:`width`,
  :code:`height`, :code:`mouse_x`, etc **are not** treated as constants.

* The "P" prefix has been dropped from the class names. So,
  :code:`PVector` becomes :code:`Vector`, :code:`PImage` becomes
  :code:`Image`, etc.

We've also renamed a couple of things:

* Processing's :code:`map()` method is now called :code:`remap()` to
  avoid a namespace conflict with Python's inbuilt :code:`map()`
  function.

* All :code:`get*()` and :code:`set*()` methods for objects have been
  removed and attributes can be set/read by directly accessing the
  objects.

  For instance, if we have a vector :code:`vec` in Processing, we
  would use

  .. code:: java

     /* read the magnitude of the vector */
     float m = vec.mag()

     /* set the magnitude of the vector */
     vec.setMag(newMagnitude)

  In p5, we can just use:

  .. code:: python

     # read the magnitude of the vector
     m = vec.magnitude

     # set the magnitude of the vector
     vec.magnitude = new_magnitude

* Processing's :code:`random()` method is now called
  :code:`random_uniform()` to prevent confusion (and nasty errors!)
  while using Python's :code:`random` module.


Running Sketches
================

* p5 doesn't come with an IDE and p5 scripts are run as any other
  Python scripts/programs. You are free to use any text editor or
  Python IDE to run your programs.

* Sketches **must** call the :code:`run()` function to actually
  show the sketches. Sketches without a call to :code:`run()` **will
  not work**. So, a Processing sketch:

  .. code:: java

     void setup() {
         /* things to do in setup */
     }

     void draw() {
         /* things to do in the draw loop */
     }

     void mousePressed() {
         /* things to do when the mouse is pressed */
     }

  would look like this in p5:

  .. code:: python

     from p5 import *

     def setup():
         # Things to do in setup

     def draw():
         # Things to do in the draw loop

     def mouse_pressed():
         # Things to do when the mouse is pressed.

     run() # This is essential!

* Drawing commands only work inside functions.

* If you want to control the frame rate of the you need to pass in
  :code:`frame_rate` asnan optional argument when you run your sketch.

  .. code:: python

     from p5 import *

     def setup():
         # setup code

     def draw():
         # draw code

     # run the sketch at 15 frames per second.
     run(frame_rate=15)



* Processing's :code:`frameRate()` method is called
  :code:`set_frame_rate()` in p5. To get the current frame rate in the
  sketch, use the :code:`frame_rate` global variable.

Shapes, etc
===========

* One of the major differences between the Processing and the p5 API
  is the way coördinate points are handled. With the exception of the
  `point()` functions, all drawing functions that allow the user to
  pass in coordinates use tuples.

  Hence, to draw a line from :math:`(100, 100)` to :math:`(180, 180)`,
  we would use:

  .. code:: python

     start_point = (100, 100)
     end_point = (180, 180)

     line(start_point, end_point)

  To draw a rectangle at :math:`(90, 90)` with width :math:`100` and
  height :math:`45`, once would use:

  .. code:: python

     location = (90, 90)
     rect(location, 100, 45)

  Technically, any object that supports indexing (lists, p5 Vectors)
  could be used as the coordinates to the draw calls. Hence, the
  following code snippet is perfectly valid:

  .. code:: python

     start_point = Vector(306, 72)
     control_point_1 = Vector(36, 36)
     control_point_2 = Vector(324, 324)
     end_point = Vector(54, 288)

     bezier(start_point, control_point_1, control_point_2, end_point)

* Functions like `bezier_point`, `bezier_tangent`, `curve_point`,
  `curve_tangent`, etc also need the coordinates as iterables.
  Further, they also return special objects that have :math:`x, y, z`
  coordinates.

  .. code:: python

     start = Vector(306, 72)
     control_1 = Vector(36, 36)
     control_2 = Vector(324, 324)
     end = Vector(54, 288)

     bp = bezier_point(start, control_1, control, end, 0.5)

     # The x coordinate of the bezier point:
     print(bp.x)

     # The y coordinate of the bezier point:
     print(bp.y)

* Unlike Processing, p5 doesn't have special global constants for
  "modes". Functions like :code:`ellipse_mode()` and
  :code:`rect_mode()` take strings (in all caps) as inputs. The
  following are valid function calls:

  .. code:: python

     center = (width / 2, height / 2)

     rect_mode('RADIUS')
     square(center, 50)

     ellipse_mode('CENTER')
     circle(center, 100)

* Processing's :code:`pushMatrix()` and :code:`popMatrix()` have been
  replaced by a single :code:`push_matrix()` context manager that
  cleans up after itself. So, the following Procecssing code:

  .. code:: java

     pushMatrix()

     translate(width/2, height/2)
     point(0, 0)

     popMatrix()

  Becomes:

  .. code:: python

     with push_matrix():
         translate(width / 2, height / 2)
         point(0, 0)

* Like :code:`push_matrix()`, :code:`push_style()` is a context manager
  and can be used with the :code:`with` statement.


Event System
============

* Processing's :code:`mousePressed` global boolean has been renamed to
  :code:`mouse_is_pressed` to avoid namespace conflicts with the user
  defined :code:`mouse_pressed` function.

* To check which mouse button was pressed, compare the
  :code:`mouse_button` global variable to one of the strings
  :code:`'LEFT', 'RIGHT', 'CENTER', 'MIDDLE'`

* The :code:`keyCode` variable has been removed. And Processing's
  special "coded" keys can be compared just like other alpha numeric
  keys.

  .. code:: python

     def key_pressed(event):
         if event.key == 'A':
             # code to run when the <A> key is presesed.

         elif event.key == 'UP':
             # code to run when the <UP> key is presesed.

         elif event.key == 'SPACE':
             # code to run when the <SPACE> key is presesed.

         # ...etc

Math
====

* Vector addition, subtraction, and equality testing are done using
  the usual mathematical operators and scalar multiplication is done
  using the usual :code:`*` operator. The following are valid vector
  operations:

  .. code:: python

     # add two vectors `position` and `velocity`
     position = position + velocity

     # subtract the vector `offset` from `position`
     actual_location = position - offset

     # scale a vector by a factor of two
     scaled_vector = 2 * vec_1

     # check if two vectors `player_location`
     # and `mouse_location` are equal
     if (player_location == mouse_location):
         end_game()

     # ...etc.

* The mean and standard deviation value can be specified while calling
  :code:`random_gaussian()`

* The distance function takes in two tuples as inputs. So, the
  following Processing call:

  .. code:: java

     d = dist(x1, y1, z1, x2, y2, z2)


  would become:

  .. code:: python

     point_1 = (x1, y1, z1)
     point_2 = (x2, y2, z2)

     d = dist(point_1, point_2)

* The :code:`remap()` also takes tuples for ranges. The Processing call:

  .. code:: java

     n = map(mouseX, 0, width, 0, 10)

  becomes:

  .. code:: python

     source = (0, width)
     target = (0, 10)

     n = remap(mouse_x, source, target)


New Features
============

* The :code:`title()` method can be used to set the title for the
  sketch window.

* :code:`circle()` and :code:`square()` functions draw circles and
  squares.

* :code:`mouse_is_dragging` is a global variable that can be used to
  check if the mouse is being dragged.

* Colors can be converted to their proper grayscale values.

  .. code:: python

     # if we have some color value...
     our_color = Color(255, 127, 0)

     # ...we can get its gray scale value
     # using its `gray` attribute
     gray_value = our_color.gray
