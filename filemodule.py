from datetime import datetime
from logger import *
import json
import os


def read_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def write_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def make_backup(data):
    now = datetime.now().timestamp()
    write_data(f"backup{str(now)}.json", data)
