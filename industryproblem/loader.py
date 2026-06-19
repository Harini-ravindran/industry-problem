import json

def load_tariffs(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Invalid JSON File")
        return None