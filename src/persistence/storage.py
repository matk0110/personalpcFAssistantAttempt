class PersistenceManager:
    def __init__(self, filename='data/state.json'):
        self.filename = filename
        self.data = {}

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
        except json.JSONDecodeError:
            self.data = {}

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def auto_save(self):
        self.save()

    def set_data(self, key, value):
        self.data[key] = value
        self.auto_save()

    def get_data(self, key):
        return self.data.get(key, None)