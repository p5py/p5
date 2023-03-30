# This file adds Processing API compatibility for p5py

from typing import Dict
from .http_data import http_post, http_get
from .local_data import load_table


def httpGet(url: str):
    """
    Performs a synchronous GET request on the given url.

    :param url: url of the API

    """
    return http_get(url)


def httpPost(url: str, postData: Dict):
    """
    Performs a synchronous POST request on the given url.

    :param url: url of the API
    :param postData: Key-value pairs of the request payload.

    """
    return http_post(url, postData)


def loadTable(path: str, mode: str = "csv"):
    """
    Calls Table class and returns a Table class object

    :param path: Path to file

    :param mode: Type of File csv/ssv/tsv.

    :returns: A table object

    """
    return load_table(path, mode)
