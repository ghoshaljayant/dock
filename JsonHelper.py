import json

def read_json_file(json_path):
    try:
        with open(json_path, 'r', encoding="utf-8") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(e)