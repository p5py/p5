************
Array Object
************

.. raw:: html

  <script>

	class Module {
	    constructor(xOff, yOff, x, y, speed, unit) {
	        this.xOff = xOff;
	        this.yOff = yOff;
	        this.x = x;
	        this.y = y;
	        this.speed = speed;
	        this.unit = unit;
	        this.xDir = 1;
	        this.yDir = 1;
	    }

	    // Custom method for updating the variables
	    update() {
	        this.x = this.x + this.speed * this.xDir;
	        if (this.x >= this.unit || this.x <= 0) {
	            this.xDir *= -1;
	            this.x = this.x + 1 * this.xDir;
	            this.y = this.y + 1 * this.yDir;
	        }
	        if (this.y >= this.unit || this.y <= 0) {
	            this.yDir *= -1;
	            this.y = this.y + 1 * this.yDir;
	        }
	    }

	    // Custom method for drawing the object
	    draw() {
	        fill(255);
	        ellipse(this.xOff + this.x, this.yOff + this.y, 6, 6);
	    }
	}

	let unit = 40;
	let count;
	let mods = [];

	function setup() {
	    var canvas = createCanvas(720, 360);
  	  	canvas.parent('sketch-holder');
	    noStroke();
	    let wideCount = width / unit;
	    let highCount = height / unit;
	    count = wideCount * highCount;

	    let index = 0;
	    for (let y = 0; y < highCount; y++) {
	        for (let x = 0; x < wideCount; x++) {
	            mods[index++] = new Module(
	                x * unit,
	                y * unit,
	                unit / 2,
	                unit / 2,
	                random(0.05, 0.8),
	                unit
	            );
	        }
	    }
	}

	function draw() {
	    background(0);
	    for (let i = 0; i < count; i++) {
	        mods[i].update();
	        mods[i].draw();
	    }
	}
  </script>
  <div id="sketch-holder"></div>

Demonstrates the syntax for creating an array of custom objects.

.. code:: python

	from p5 import *

	unit = 40
	count = None
	mods = []

	def setup():
		size(640, 360)
		no_stroke()

		global count, unit, mods
		wideCount = width / unit
		highCount = height / unit

		count = wideCount * highCount
		index = 0
		for y in range(int(highCount)):
			for x in range(int(wideCount)):
				mods.append(Module(x*unit, y*unit, unit/2, unit/2, random_uniform(0.05, 0.8), unit))

	def draw():
		background(0)
		for mod in mods:
			mod.update()
			mod.display()

	class Module:
		def __init__(self, xOffsetTemp, yOffsetTemp, xTemp, yTemp, speedTemp, tempUnit):
			self.xOffset = xOffsetTemp
			self.yOffset = yOffsetTemp

			self.x = xTemp
			self.y = yTemp
			self.speed = speedTemp
			self.unit = tempUnit

			self.xDirection = 1
			self.yDirection = 1

		def update(self):
			self.x = self.x + (self.speed * self.xDirection)
			if self.x > unit or self.x <= 0: 
				self.xDirection *= -1
				self.x += self.xDirection
				self.y += self.yDirection
			elif self.y > unit or self.y <= 0:
				self.yDirection *= -1
				self.y += yDirection

		def display(self):
			fill(255)
			ellipse((self.xOffset + self.x, self.yOffset + self.y), 6, 6)


	if __name__ == '__main__':
		run()