class StorageService:
    def __init__(self):
        self.data = {}  # dictionary to store key-value pairs

    def add_pair(self, key, value):
        if value is None or value == "":  # Checking if the value is empty or null
            print("Received empty value, deleting key: ", key, " and its value from storage if it exists")
            self.delete_value(key)
        else:
            print("Adding / Updating value for key: ", key)
            self.data[key] = value  # Adding a new key-value pair to the dictionary

    def delete_value(self, key):
        if key in self.data:
            del self.data[key]

    def get_value(self, key) -> str:
        return self.data.get(key)

