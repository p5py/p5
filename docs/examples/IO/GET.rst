********
GET
********

.. raw:: html

  <script>
	let url = 'https://api.wheretheiss.at/v1/satellites/25544'
	let data;
	let lat;
	let long;
	let data_recieved = 0;

	function setup() {
        let canvas = createCanvas(400, 400);
        canvas.parent('sketch-holder');
	  	httpGet(url, 'json', false, function (response) {
	    data = response; 
	    lat = data['latitude']
	    long = data['longitude']
	       data_recieved = 1;
	  });
	}
	function draw() {
	  background(220);
	  if (data_recieved){
	    textSize(16)
	    text('latitude = '+ lat + '\nlongitude = ' + long,100,200)
	  }
	}
  </script>
  <div id="sketch-holder"></div>
  <br>
  This examples illustrates a simple synchronous HTTP GET request on the position of the ISS and displays it on the canvas. Reloading the screen should update the coordinates of the ISS.
  <br>

.. code:: python

    from p5 import *

    def setup():
    	size(400, 400)
    	no_loop()

    def draw():
    	background(220)
    	sleep(0.5)
    	sat_data = http_get('https://api.wheretheiss.at/v1/satellites/25544')
    	lat = sat_data['latitude']
    	log = sat_data['longitude']
    	print(lat,log)
    	fill(0)
    	text("  latitude = " + str(lat) + "  longitude = " + str(log),(0,200))

    run(mode='P3D')