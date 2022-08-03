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
        resp = request.urlopen(url)

        data = resp.read().decode("UTF-8")

        self.text = data

        try:
            self.json = json.loads(data)
        except json.JSONDecodeError:
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
