"""
Part of the io library. Includes functions that require **internet** connection.
"""

from urllib import request
import json
import requests

# Synchronous

class http_get:
    """
    Performs a synchronous GET request on the given url.

    :param url: url of the API
    :type url: string

    """

    def __init__(self, url):
        try:
            resp = request.urlopen(url)
        except:
            print("Invalid url. Connection Failed.")
            exit(1)

        data = resp.read().decode("UTF-8")

        self.text = data
        try:
            self.json = json.loads(data)
        except: 
            self.json = data

# Synchronous

def http_post(url, post_data):
    """
    Performs a synchronous POST request on the given url.

    :param url: url of the API
    :type url: string
    :param post_data: Key-value pairs of the request payload.
    :type post_data: dict

    """
    data = requests.post(url, post_data)
    data = data.json()
    return data
    