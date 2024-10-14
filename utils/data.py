import pandas as pd
import json
import os

def save_data(data, filename):
    with open(f'./data/{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)

def is_file_exists(filename):
    return os.path.isfile(f'./data/{filename}.json')

def load_data(filename):
    with open(f'./data/{filename}.json', 'r') as f:
        return json.load(f)