"""
Part of the io library. Includes functions that require **internet** connection.
"""

from typing import Dict
from urllib import request
import json
import requests

# Synchronous


class http_get:
    """
    Performs a synchronous GET request on the given url.

    :param url: url of the API

    """

    def __init__(self, url: str):
        resp = request.urlopen(url)

        data = resp.read().decode("UTF-8")

        self.text = data

        try:
            self.json = json.loads(data)
        except json.JSONDecodeError:
            self.json = data


# Synchronous


def http_post(url: str, post_data: Dict):
    """
    Performs a synchronous POST request on the given url.

    :param url: url of the API
    :param post_data: Key-value pairs of the request payload.

    """
    data = requests.post(url, post_data)
    data = data.json()
    return data
