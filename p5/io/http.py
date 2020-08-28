from urllib import request,parse
import json
import requests

#synchronous
def http_get(url):
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
	data = requests.post(url,post_data)
	data = data.json()
	return data


