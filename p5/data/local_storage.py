import pathlib
import pickle
import os

local_storage_path = os.path.join(pathlib.Path.home(), ".p5pyStorage")

if not os.path.isdir(local_storage_path):
    os.mkdir(local_storage_path)

def get_item(key):
    item_file_path = os.path.join(local_storage_path, key)
    if os.path.isfile(item_file_path):
        with open(item_file_path, "rb") as f:
            return pickle.load(f)
    else:
        return None

def set_item(key, data):
    item_file_path = os.path.join(local_storage_path, key)

    if os.path.isfile(item_file_path):
        os.remove(item_file_path)

    with open(item_file_path, 'wb') as f:
        pickle.dump(data, f)

def remove_item(key):
    item_file_path = os.path.join(local_storage_path, key)

    if os.path.isfile(item_file_path):
        os.remove(item_file_path)

def clear_storage():
    if(os.path.isdir(local_storage_path)):
        for filename in os.listdir(local_storage_path):
            file_path = os.path.join(local_storage_path, filename)
            os.remove(file_path)
