Installation
============

p5 requires Python 3. If you don't have Python and/or are still
running Python 2, please download the Python 3 first. `The
Hitchhiker's Guide To Python <http://docs.python-guide.org/>`_ has an
excellent `section on installing Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_ that
you should refer to.

Once you have Python 3 installed, you can proceed to install p5.

pip install p5
--------------

p5 requires numpy to run, so install that first.

.. code:: bash

   $ pip install numpy

If the numpy installation fails, you might consider getting the
`Anaconda Python distribution <https://www.continuum.io/downloads>`_
and then trying to install p5. Once numpy as been successfully
installed, you can proceed to install p5:

.. code:: bash

   $ pip install numpy --user
   $ pip install p5 --user
