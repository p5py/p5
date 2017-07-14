=====
Input
=====


All user defined event handlers (`mouse_pressed`, `key_pressed`, etc)
can be defined to accept an optional event object as a positional
argument. If the user doesn't want to use extra information about the
event, they can simply define the handler *without* the positional
argument:

.. code:: python

   def mouse_pressed():
       # things to do when the mouse is pressed.

If, however, the user would like to extract more information from the
event, they can define their function as follows:

.. code:: python

   def mouse_pressed(event):
       # things to do when the mouse is pressed.

This event object has special methods that can be used to access
additional details about the event. All events support the following methods:


- :code:`event.is_shift_down()`: Returns :code:`True` when the shift
  key is held down when the event occurs.

- :code:`event.is_ctrl_down()`: Returns :code:`True` when the ctrl key
  is held down when the event occurs.

- :code:`event.is_alt_down()`: Returns :code:`True` when the alt key
  is held down when the event occurs.

- :code:`event.is_meta_down()`: Returns :code:`True` when the meta key
  is held down when the event occurs.

For mouse events, this event object has some more additional attributes:

- :code:`event.x`: The x position of the mouse at the time of the event.

- :code:`event.y`: The y position of the mouse at the time of the event.

- :code:`event.position`: A named tuple that stores the position of
  the mouse at the time of the event. The x and the y positions can
  also be accessed using :code:`event.position.x` and
  :code:`event.position.y` respectively.

- :code:`event.change`: A named tuple that stores the changes (if any)
  in the mouse position at the time of the event. The changes in the x
  and the y direction can be accessed using :code:`event.change.x` and
  :code:`event.change.y`.

- :code:`event.scroll`: A named tuple that stores the scroll amount
  (if any) at the mouse position at the time of the event. To access
  the scroll amount in the x and the y direction, use
  :code:`event.scroll.x` and :code:`event.scroll.y` respectively.

- :code:`event.count`: An integer that stores the scroll in the y
  direction at the time of the event. Positive values indicate
  "scroll-up" and negative values "scroll-down".

- :code:`event.button`: The state of the mouse button(s) at the time
  of the event. It's behavior is similar to the :code:`mouse_button`
  global variable.

- :code:`event.action`: Stores the "action type" of the current event.
  Depending on the event, this can take on one of the following
  values:

  * :code:`'PRESS'`
  * :code:`'RELEASE'`
  * :code:`'CLICK'`
  * :code:`'DRAG'`
  * :code:`'MOVE'`
  * :code:`'ENTER'`
  * :code:`'EXIT'`
  * :code:`'WHEEL'`

For key events, the event object has the following attributes:

- :code:`event.action`: Stores the "action type" for the current key
  event. This can take on the following values:

  * :code:`'PRESS'`
  * :code:`'RELEASE'`
  * :code:`'TYPE'`

- :code:`event.key`: Stores the key associated with the current key
  event. Its behavior is similar to the global `key` object.


Mouse
=====

mouse_moved()
-------------

The user defined event handler that is called when the mouse is moved.

mouse_pressed()
---------------

The user defined event handler that is called when any mouse button is
pressed.

mouse_released()
----------------

The user defined event handler called when a mouse button is released.

mouse_clicked()
---------------

The user defined event handler that is called whent the mouse has been
clicked. The :code:`mouse_clicked` handler is called after the mouse
has been pressed and then released.

mouse_dragged()
---------------

The user defined event handler called when the mouse is being dragged.
Note that this is called *once* when the mouse has started dragging.
To check if the mouse is still being dragged use the
:code:`mouse_is_dragging` global variable.


mouse_wheel()
-------------

The user defined event handler that is called when the mouse scroll
wheel is moved.

mouse_is_pressed
----------------

`mouse_is_pressed` is a global boolean that stores whether or not a
mouse button is curretnly being pressed. More information about the
actual button being pressed is stored in the `mouse_button` global
variable. It is set to `True` when any mouse button is held down and
is `False` otherwise.

.. code:: python

   if mouse_is_pressed:
       # code to run when the mouse button is held down.

mouse_is_dragging
-----------------

`mouse_is_dragging` is a global boolean that stores whether or not the
mouse is currently being dragged. When the mouse is being dragged,
this variable is set to `True` and has a value of `False` otherwise.

.. code:: python

   if mouse_is_dragging:
       # code to run when the mouse is being dragged.

mouse_button
------------

`mouse_button` is a global object that stores information about the
current mouse button that is being held down. If no button is being
held down, `mouse_button` is set to `None`. `mouse_button` can be
compared to the strings `'MIDDLE'`, `'CENTER'`, `'LEFT'`, or `'RIGHT'`
to check which mouse button is being held down.

.. code:: python

   if mouse_button == 'CENTER':
       # code to run when the middle mouse button is pressed.

   elif mouse_button == 'LEFT':
       # code to run when the left mouse button is pressed.

   elif mouse_button == 'RIGHT':
       # code to run when the right mouse button is pressed.


mouse_x, mouse_y
----------------

Global variables that store the x and the y positions of the mouse for
the **current** draw call.

pmouse_x, pmouse_y
------------------

Global variables that store the x and the y positions of the mouse for
the **last** draw call.

Keyboard
========

key
---

A global variable that keeps track of the current key being pressed
(if any). This is set to :code:`None` when no key is being pressed.
This can be compared to different strings to get more information
about the key. These strings should be the names of the keys --- like
'ENTER', 'BACKSPACE', 'A', etc --- and should always be in uppercase.

For instance:

.. code:: python

   if key == 'UP':
       # things to do when the up-key is held down.

   elif key == 'ENTER':
       # things to do when the enter/return key is pressed

   elif key == '1':
       # things to do when the "1" key is pressed.

   # etc...


key_is_pressed
--------------

A global boolean that keeps track of whether *any* key is being held
down. This is set to :code:`True` is some key is held down and
:code:`False` otherwise.

key_pressed()
-------------

A user defined event handler that is called when a key is pressed.

key_released()
--------------

A user defined event handler that is called when a key is released.

key_typed()
-----------

A user defined event handler that is called when a key is typed.
