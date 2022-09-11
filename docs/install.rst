Installation
============

Prerequisites: Python
---------------------

p5 requires Python 3.6 or above. Most recent versions of MacOS and Linux systems
should have an installation of Python already. If you're not sure
which version your computer is using, run

.. code-block:: bash

   python --version

from a terminal window. If the reported version is greater than 3.6,
you're good to proceed.

If you don't already have Python installed, refer to the `The
Hitchhiker's Guide To Python <http://docs.python-guide.org/>`_ and its
`section on Python installation
<http://docs.python-guide.org/en/latest/starting/installation/>`_.
Alternatively, on Windows, you can also consider installing Python
through the `Miniconda Python installer
<https://conda.io/miniconda.html>`_.

Prerequisites: GLFW
-------------------

Internally p5 uses `GLFW <http://www.glfw.org/>`_ to handle window
events and to work with OpenGL graphics.

Windows
^^^^^^^

First, download and install the pre-compiled Windows binaries from the
official `GLFW downloads page <http://www.glfw.org/download.html>`_.
During the installation process, make sure to take note of the folder
where GLFW.

Finally, the GLFW installation directory should be added to the
`system path <https://en.wikipedia.org/wiki/PATH_(variable)>`_. Make
sure to add containing the .dll and .a files
(for example: `\\<path to glfw>\\glfw-3.2.1.bin.WIN64\\lib-mingw-w64`)

First locate the "Environment Variables" settings dialog box. On
recent versions of Windows (Windows 8 and later), go to System info >
Advanced Settings > Environment Variables. On older versions (Windows
7 and below) first right click the computer icon (from the desktop or
start menu) and then go to Properties > Advanced System Settings >
Advanced > Environment Variables. Now, find and highlight the "Path"
variable and click the edit button. Here, add the GLFW installation
directory to the end of the list and save the settings.

MacOS, Linux
^^^^^^^^^^^^

Most package systems such as `homebrew`, `aptitude`, etc already have
the required GLFW binaries. For instance, to install GLFW on Mac using
homebrew, run

.. code:: bash

   $ brew install glfw


Similarly, on Debain (and it's derivatives like Ubuntu and Linux
Mint)run

.. code:: bash

   $ sudo apt-get install libglfw3

For other Linux based systems, find and install the GLFW package using
the respective package system.

Installing p5
-------------

The p5 installer should automatically install the required
dependencies (mainly numpy and vispy), so run

.. code:: bash

   $ pip install p5 --user

to install the latest p5 version

You could also install p5 from git directly to get the latest features, yet to be released.

.. code:: bash

   $ pip install git+https://github.com/p5py/p5.git#egg=p5

or you could clone the repository and install it.

.. code:: bash

   $ git clone https://github.com/p5py/p5.git
   $ cd p5
   $ pip install .

We also recommend you to setup a virtual environment to avoid any dependencies conflicts. You can use this `virtual environment primer <https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment>`_

**NOTE**: p5 now has a new 2D renderer in beta stage, that could be used by specifying the renderer in run().

.. code:: python

   from p5 import *
   # .
   # .
   # .
   run(renderer='skia')

Troubleshooting
---------------

1. In case the automatically
installation fails, try installing the dependencies separately:

.. code:: bash

   $ pip install numpy
   $ pip install vispy

2. If you get a error that says ``Microsoft Visual C++ is required`` then follow the below steps:

- Install the prebuilt version of vispy from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#vispy. For instance if you have python 3.8 then download the cp38 one.

- Open terminal and cd into the directory in which you downloaded the prebuilt vispy file.

- Then in terminal type:
    .. code:: bash

        $ pip install file_downloaded.whl
        $ pip install p5 --user

In case of other installation problems, open an issue on the main `p5
Github <https://github.com/p5py/p5/issues>`_ repository.


