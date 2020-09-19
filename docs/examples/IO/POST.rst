************
POST
************

.. raw:: html

    <script>
	function setup() { 
    let canvas = createCanvas(400, 400);
    canvas.parent('sketch-holder');
	background(220);
	postRequest();
	}
	function postRequest() { 
	let api_url = 'https://reqres.in/api/users'; 
	let postData = { id: 1, name: "Sam", email: "sam@samcorp.com" }; 
	httpPost(api_url, 'json', postData, function (response) { 
		text("Data returned from API", 20, 100); 
		text("The ID in the data is: " + response.id, 20, 140); 
		text("The Name in the data is: " + response.name, 20, 160); 
		text("The Email in the data is: " + response.email, 20, 180); 
	}); 
	}
    </script>
    <div id="sketch-holder"></div>
    This example illustrates a simple synch POST request.
    <br>

.. code:: python

    from p5 import *

    def setup():
    	background(220)
        size(400, 400)
        postrequest()
        no_loop()

    def postrequest():
    	data = { 'id': '1', 'name': "Sam", 'email': "sam@samcorp.com" }
    	response = http_post('https://reqres.in/api/users',data)
    	print(response)
    	
    run(mode='P3D')
