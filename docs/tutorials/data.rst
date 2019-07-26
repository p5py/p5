****
Data
****

:Authors: Daniel Shiffman; Arihant Parsoya (p5 port)

:Copyright: This tutorial is from the book `Learning Processing, 
   2nd Edition <https://processing.org/books/#shiffman>`_, published by MIT
   Press. © 2014 MIT Press. If you see any errors or have comments,
   please let us know. The tutorial was ported to p5 by Arihant Parsoya. If
   you see any errors or have comments, open an issue on either the
   `p5 <https://github.com/p5py/p5/issues>`_ or `Processing
   <https://github.com/processing/processing-docs/issues?q=is%3Aopen>`_
   repositories.

This tutorial picks up where the Strings and Drawing Text tutorial leaves off and examines how to use String objects as the basis for reading and writing data. We'll start by learning more sophisticated methods for manipulating Strings, searching in them, chopping them up, and joining them together. Afterwards, we'll see how these skills allow us to use input from data sources, such as text files, web pages, xml feeds, and 3rd party APIs and take a step into the world of data visualization.

Manipulating Strings
====================

In Strings and Drawing Text, we touched on a few of the basic functions available in the Java String, such as upper() and len(). These functions are documented on the Processing reference page for Strings. Nevertheless, in order to perform some more advanced data parsing techniques, we'll need to explore some additional String manipulation functions documented in the Python API. 

Let's take a closer look at the following two String functions: index() and slicing.

index() locates a sequence of characters within a string. It takes one argument — a search string — and returns a numeric value that corresponds to the first occurrence of the search string inside of the String object being searched.

.. code:: python

	search = "def"
	toBeSearched = "abcdefghi"
	index = toBeSearched.index(search) # The value of index in this example is 3.

Strings are just like arrays, in that the first character is index number zero and the last character is the length of the string minus one. If the search string cannot be found, index() returns -1. This is a good choice because -1 is not a legitimate index value in the string itself, and therefore can indicate "not found." There are no negative indices in a string of characters or in an array. 

Strings are just like arrays, in that the first character is index number zero and the last character is the length of the string minus one. If the search string cannot be found, ValueError is returned by the program.

After finding a search phrase within a string, we might want to separate out part of the string, saving it in a different variable. A part of a string is known as a substring and substrings are made by slicing the array using two arguments, a start index and an end index. slicing the array returns the substring in between the two indices.

.. code:: python

	alphabet = "abcdefghi"
	sub = alphabet[3:6] # The String sub is now "def".

Note that the substring begins at the specified start index (the first argument) and extends to the character at end index (the second argument) minus one. I know, I know. Wouldn’t it have been easier to just take the substring from the start index all the way to the end index? While this might initially seem true, it’s actually quite convenient to stop at end index minus one. For example, if you ever want to make a substring that extends to the end of a string, you can simply go all the way to len(thestring). In addition, with end index minus one marking the end, the length of the substring is easily calculated as end index minus begin index.

Splitting and Joining Strings
=============================

In Strings and Drawing Text, we saw how strings can be joined together (referred to as "concatenation") using the "+" operator. Let's review with a example that uses concatenation to get user input from a keyboard. 

.. image:: ./data-res/fig_18_01_user_input.png
   :align: center

.. code:: python

	from p5 import *

	f = None 
	# Variable to store text currently being typed
	typing = ""
	# Variable to store saved text when return is hit
	saved = ""

	def setup():
		global f
		size(300,200)
		f = create_font("Arial.ttf", 16)

	def draw():
		global f
		background(255)

		indent = 25

		# Set the font and fill for text
		text_font(f)
		fill(0)

		# Display everything  
		text("Click in this sketch and type. \nHit return to save what you typed.", (indent, 40))
		text(typing, (indent, 90))
		text(saved, (indent, 130))

	def key_pressed():
		global typing, saved
		# If the return key is pressed, save the String and clear it 
		if key == "ENTER":
			saved = typing
			typing = ""
		else: # Otherwise, concatenate the String 
			typing = typing + str(key)

	if __name__ == '__main__':
		run()

Processing has two additional functions that make joining strings (or the reverse, splitting them up) easy. In sketches that involve parsing data from a file or the web, you might get hold of that data in the form of an array of strings or as one long string. Depending on what you want to accomplish, it’s useful to know how to switch between these two modes of storage. This is where these two new functions, split() and join(), will come in handy.

**"one long string or array of strings" ←→ {"one", "long", "string", "or" ,"array", "of", "strings"}**

Let’s take a look at the split() function. split() separates a longer string into an array of strings, based on a split character known as the delimiter. It takes the delimiter as the argument. (The delimiter can be a single character or a string.) In the code below, the period is not set as a delimiter and therefore will be included in the last string in the array: “dog.” Note how printArray() can be used to print the contents of an array and their corresponding indices to the message console.	

.. code:: python

	# Splitting a string based on spaces
	spaceswords = "The quick brown fox jumps over the lazy dog."
	list = spaceswords.split(" ")
	print(list)

Here is an example using a comma as the delimiter (this time passing in a single character: ','.)	

.. code:: python

	# Splitting a string based on commas
	commaswords = "The,quick,brown,fox,jumps,over,the,lazy,dog."
	list = commaswords.split(",")

If you are splitting numbers in a string, the resulting elements of the array can be converted into an integer array with Python's int() function. Numbers in a string are not numbers and cannot be used in mathematical operations unless you convert them first.

.. code:: python

	# Calculate sum of a list of numbers in a String
	numbers = "8,67,5,309"
	# Converting the String array to an int array
	list = numbers.split(",")
	sum = 0
	for i in list:
		sum += int(i)

	print(sum)

The reverse of split() is join(). join() takes an array of strings and joins them together into one long String object. The join() function also takes two arguments, the array to be joined and a separator. The separator can either be a single character or a string of characters.

.. code:: python

	 lines = ["It", "was", "a", "dark", "and", "stormy", "night."]

Using the “+” operator along with a for loop, you can join a string together as follows:

.. code:: python

	# Manual Concatenation
	onelongstring = ""

	for i in lines:
		onelongstring += i + " "

The join() function, however, allows you to bypass this process, achieving the same result in only one line of code.

.. code:: python

	onelongstring = " ".join(lines)

Dealing with Data
=================

Data can come from many different places: websites, news feeds, spreadsheets, databases, and so on. Let's say you've decided to make a map of the world's flowers. After searching online you might find a PDF version of a flower encyclopedia, or a spreadsheet of flower genera, or a JSON feed of flower data, or a REST API that provides geolocated lat/lon coordinates, or some web page someone put together with beautiful flower photos, and so on and so forth. The question inevitably arises: “I found all this data; which should I use, and how do I get it into Processing?”

If you are really lucky, you might find a Processing library that hands data to you directly with code. Maybe the answer is to just download this library and write some code like:

.. code:: python

	import flowers

	void setup():
		fdb = FlowerDatabase()
		sunflower = fdb.findFlower("sunflower")
		h = sunflower.getAverageHeight()

In this case, someone else has done all the work for you. They've gathered data about flowers and built a Processing library with a set of functions that hands you the data in an easy-to-understand format. This library, sadly, does not exist (not yet), but there are some that do. For example, YahooWeather is a library by Marcel Schwittlick that grabs weather data from Yahoo for you, allowing you to write code like weather.getWindSpeed() or weather.getSunrise() and more. There is still plenty of work to do in the case of using a library.

Let's take another scenario. Say you’re looking to build a visualization of Major League Baseball statistics. You can't find a Processing library to give you the data but you do see everything you’re looking for at mlb.com. If the data is online and your web browser can show it, shouldn't you be able to get the data in Processing? Passing data from one application (like a web application) to another (say, your Processing sketch) is something that comes up again and again in software engineering. A means for doing this is an API or “application programming interface”: a means by which two computer programs can talk to each other. Now that you know this, you might decide to search online for “MLB API”. Unfortunately, mlb.com does not provide its data via an API. In this case you would have to load the raw source of the website itself and manually search for the data you’re looking for. While possible, this solution is much less desirable given the considerable time required to read through the HTML source as well as program algorithms for parsing it.

Each means of getting data comes with its own set of challenges. The ease of using a Processing library is dependent on the existence of clear documentation and examples. But in just about all cases, if you can find your data in a format designed for a computer (spreadsheets, XML, JSON, etc.), you'll be able to save some time in the day for a nice walk outside.

One other note worth a mention about working with data. When developing an application that involves a data source, such as a data visualization, it’s sometimes useful to develop with “dummy” or “fake” data. You don't want to be debugging your data retrieval process at the same time as solving problems related to algorithms for drawing. In keeping with my one-step-at-a-time mantra, once the meat of the program is completed with dummy data, you can then focus solely on how to retrieve the actual data from the real source. You can always use random or hard-coded numbers into your code when you’re experimenting with a visual idea and connect the real data later.

Working with Text Files
=======================

Let's begin by working with the simplest means of data retrieval: reading from a text file. Text files can be used as a very simple database (you could store settings for a program, a list of high scores, numbers for a graph, etc.) or to simulate a more complex data source.

In order to create a text file, you can use any simple text editor. Windows Notepad or Mac OS X TextEdit will do; just make sure you format the file as “plain text.” It is also advisable to name the text files with the “.txt” extension, to avoid any confusion. And just as with image files, these text files should be placed in the sketch’s “data” directory in order for them to be recognized by the Processing sketch.

Once the text file is in place, Python's open() function is used to read the content of the file into a String array. The individual lines of text in the file each become an individual element in the array. 

.. image:: ./data-res/fig_18_02_filetxt.png
   :align: center

.. code:: python
	
	# This code will print all the lines from the source text file.
	lines = open("file.txt", "r").read()
	print("There are " + len(lines) + " lines.")
	print(lines)

To run the code, create a text file called “file.txt,” type a bunch of lines in that file, and place it in your sketch’s data directory.

Text from a file can be used to generate a simple visualization. Take the following data file. 

.. image:: ./data-res/fig_18_03_datatxt.png
   :align: center

The results of visualizing this data are shown below.
**Graphing Comma-Separated Numbers from a Text File**

.. image:: ./data-res/fig_18_04_bargraph.png
   :align: center

.. code:: python

	from p5 import *

	data = []

	def setup():
		global data
		size(200,200)
		# Load text file as a String
		stuff = loadStrings("data.csv")
		# Convert string into an array of integers using ',' as a delimiter
		for i in stuff[0].split(","):
			data.append(i)

	def draw():
		global data
		background(255)
		stroke(0)

		for i in data:
			# Use array of ints to set the color and height of each rectangle.
			rect((i*20, 0), 20, data[i])

		no_loop()

	if __name__ == '__main__':
		run()

Looking at how to parse a csv file with ``split()`` was a nice learning exercise. In truth, dealing with csv files (which can easily be generated from spreadsheet software such as Google docs) is such a common activity that Processing has an entire built-in class called Table to handle the parsing for you.

Tabular Data
============

A table consists of data arranged as a set of rows and columns, also called “tabular data.” If you've ever used a spreadsheet, this is tabular data. Processing's loadTable() function takes comma-separated (csv) or tab-separated (tsv) values and automatically places the contents into a Table object storing the data in columns and rows. This is a great deal more convenient than struggling to manually parse large data files with split(). It works as follows. Let's say you have a data file that looks like:

.. image:: ./data-res/fig_18_05_datacsv.png
   :align: center

Instead of saying:

.. code:: python

	stuff = loadStrings("data.csv")

We can now say:

.. code:: python

	table = loadTable("data.csv")

Now I've missed an important detail. Take a look again at the data.csv text file above. Notice how the first line of text is not the data itself, but rather a header row. This row includes labels that describe the data included in each subsequent row. The good news is that Processing can automatically interpret and store the headers for you, if you pass in the option "header" when loading the table. (In addition to "header", there are other options you can specify. For example, if your file is called data.txt but is comma separated data you can pass in the option "csv". If it also has a header row, then you can specifiy both options like so: "header,csv").

.. code:: python

	 table = loadTable("data.csv", "header");

Now that the table is loaded, I can show how you grab individual pieces of data or iterate over the entire table. Let's look at the data visualized as a grid. 

.. image:: ./data-res/data_05_headers.jpg
   :align: center

In the above grid you can see that the data is organized in terms of rows and columns. One way to access the data, therefore, would be to request a value by its numeric row and column location (with zero being the first row or first column). This is similar to accessing a pixel color at a given (x,y) location, though in this case the y position (row) comes first. The following code requests a piece of data at a given (row, column) location.

