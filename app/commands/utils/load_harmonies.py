import json
import os

def load_harmonies():
    data_path = os.path.join(os.path.dirname(__file__), "../../../data/harmonies.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)