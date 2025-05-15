import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

class Config:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

config = Config()
