import json


class StorageService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.load_data_from_file()

    def add_pair(self, key, value):
        if value is None or value == "":
            print("Received empty value, deleting key: ", key, " and its value from storage if it exists")
            self.delete_value(key)
        else:
            print("Adding / Updating value for key: ", key, " With value: ", value)
            self.data[key] = value
            self.save_data_to_file()

    def delete_value(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data_to_file()

    def get_value(self, key) -> str:
        return self.data.get(key)

    def load_data_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                file_content = file.read()
                if file_content:
                    self.data = json.loads(file_content)
                else:
                    self.data = {}
        except FileNotFoundError:
            pass

    def save_data_to_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)
