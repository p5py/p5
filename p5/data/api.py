# This file adds Processing API compatibility to p5py

from .local_storage import get_item, set_item, clear_storage, remove_item


def getItem(key):
    """
    Returns the value of an item that was stored int local storage using store_item(), None if not found

    :param key: key name that was used while storing data using store_item()
    :type key: string

    :returns: Value of stored item
    :rtype: object

    """
    return get_item(key)


def setItem(key, value):
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
    set_item(key, value)


def removeItem(key):
    """
    Removes an item that was stored with store_item()

    :param key: key name to remove the associated value
    :type key: string

    """
    remove_item(key)


def clearStorage():
    """
    Clears all storage items set with store_item()
    """
    clear_storage()
