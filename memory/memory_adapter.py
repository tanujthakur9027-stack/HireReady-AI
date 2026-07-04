import json
import os

MEMORY_DIR = "memory"

os.makedirs(MEMORY_DIR, exist_ok=True)


def save_memory(user, data):

    path = os.path.join(MEMORY_DIR, f"{user}.json")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old = json.load(f)
    else:
        old = {}

    old.update(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(old, f, indent=4)


def load_memory(user):

    path = os.path.join(MEMORY_DIR, f"{user}.json")

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)