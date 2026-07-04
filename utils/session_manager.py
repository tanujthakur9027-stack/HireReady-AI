import json
import os

DATA_DIR = "data/interviews"
os.makedirs(DATA_DIR, exist_ok=True)


def session_file(name):
    return os.path.join(DATA_DIR, f"{name}.json")


def save_session(name, data):
    with open(session_file(name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_session(name):
    path = session_file(name)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    return None