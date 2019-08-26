***********************
Statements and Comments
***********************

.. raw:: html

  <script>
	let y = 100;
    function setup() {
      	var canvas = createCanvas(720, 400);
		canvas.parent('sketch-holder');
		background(204, 153, 0);
    }


    </script>
    <div id="sketch-holder"></div> 


Statements are the elements that make up programs. In Python, each line is a statement. Comments are used for making notes to help people better understand programs. A comment begins with a number sign ("#").

.. code:: python

	from p5 import *

	def draw():
		# The size function is a statement that tells the computer 
		# how large to make the window.
		# Each function statement has zero or more parameters. 
		# Parameters are data passed into the function
		# and are used as values for telling the computer what to do.
		size(640, 360)

		# The background function is a statement that tells the computer
		# which color (or gray value) to make the background of the display window 
		background(204, 153, 0)

	if __name__ == '__main__':
	    run()
