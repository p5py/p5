from urllib import request
import json




def http_get(url):
	try:
		resp = request.urlopen(url)
	except Exception:
		print("Invalid url. Connection Failed.")
		exit(1)
	data = resp.read()
	data = json.loads(data.decode("UTF-8"))
	return data