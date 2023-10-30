import json

def load_data(file_path):
    with open(file_path, 'r') as data_file:
        data = [json.loads(line) for line in data_file]
    return data
