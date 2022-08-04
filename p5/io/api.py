# This file adds Processing API compatibility for p5py

from .http_data import http_post, http_get
from .local_data import load_table


def httpGet(url):
    """
    Performs a synchronous GET request on the given url.

    :param url: url of the API
    :type url: string

    """
    return http_get(url)


def httpPost(url, postData):
    """
    Performs a synchronous POST request on the given url.

    :param url: url of the API
    :type url: string
    :param postData: Key-value pairs of the request payload.
    :type postData: dict

    """
    return http_post(url, postData)


def loadTable(path, mode="csv"):
    """
    Calls Table class and returns a Table class object

    :param path: Path to file
    :type path: string

    :param mode: Type of File csv/ssv/tsv.
    :type mode: string

    :returns: A table object
    :rtype: object

    """
    load_table(path, mode)
