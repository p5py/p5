"""
 * This module defines the p5 methods for working with local storage
"""

import pathlib
import pickle
import os

local_storage_path = os.path.join(pathlib.Path.home(), ".p5pyStorage")

if not os.path.isdir(local_storage_path):
    os.mkdir(local_storage_path)


def get_item(key):
    """
    Returns the value of an item that was stored int local storage using store_item(), None if not found

    :param key: key name that was used while storing data using store_item()
    :type key: string

    :returns: Value of stored item
    :rtype: object

    """
    item_file_path = os.path.join(local_storage_path, key)
    if os.path.isfile(item_file_path):
        with open(item_file_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def set_item(key, value):
    """
    * Stores a value in local storage under the key name.
    * Local storage persists in between the p5py sketch sessions.
    * The key can be the name of the variable but doesn't have to be.
    * Sensitive data such as passwords or personal information should not be stored in local storage.
    * Overwrites the key if already present

    :param key: key name that you wish to you use in local storage
    :type key: basestring

    :param value: Value to be stored, can be of any type
    :type value: object

    """
    item_file_path = os.path.join(local_storage_path, key)

    if os.path.isfile(item_file_path):
        os.remove(item_file_path)

    with open(item_file_path, "wb") as f:
        pickle.dump(value, f)


def remove_item(key):
    """
    Removes an item that was stored with store_item()

    :param key: key name to remove the associated value
    :type key: string

    """
    item_file_path = os.path.join(local_storage_path, key)

    if os.path.isfile(item_file_path):
        os.remove(item_file_path)


def clear_storage():
    """
    Clears all storage items set with store_item()
    """
    if os.path.isdir(local_storage_path):
        for filename in os.listdir(local_storage_path):
            file_path = os.path.join(local_storage_path, filename)
            os.remove(file_path)
