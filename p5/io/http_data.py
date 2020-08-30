from urllib import request,parse
import json
import requests

#synchronous
def http_get(url):
	"""
	Performs a synchronous GET request on the given url.

	:param url: url of the API
	:type url: string

	"""
	try:
		resp = request.urlopen(url)
	except Exception:
		print("Invalid url. Connection Failed.")
		exit(1)
	data = resp.read()
	data = json.loads(data.decode("UTF-8"))
	return data

#synchronous
def http_post(url,post_data):
	"""
	Performs a synchronous POST request on the given url.

	:param url: url of the API
	:type url: string
	:param post_data: Key-value pairs of the request payload.
	:type post_data: dict 

	"""
	data = requests.post(url,post_data)
	data = data.json()
	return data


