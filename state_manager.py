import json


class StateManager:
    def __init__(self):
        self.file_path = "state.json"
        self.state = {}
        self.load_state()

    def load_state(self):
        try:
            with open(self.file_path, "r") as file:
                self.state = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty state
            self.state = {}

    def save_state(self):
        with open(self.file_path, "w") as file:
            json.dump(self.state, file)

    def get_value(self, key):
        return self.state.get(key)

    def set_value(self, key, value):
        self.state[key] = value
        self.save_state()
