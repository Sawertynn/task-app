import json
from pathlib import Path

class FileDB:
    def __init__(self, path: Path):
        self.path = path

    def load(self):
        # TODO: check path
        with open(self.path, 'r') as file:
            return json.load(file)
        
    def save(self, data):
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=2)