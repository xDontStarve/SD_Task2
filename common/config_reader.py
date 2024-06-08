import yaml

class ConfigReader:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.config_data = yaml.safe_load(file)

    def get_master_ip(self):
        return self.config_data['master']['ip']

    def get_master_port(self):
        return self.config_data['master']['port']

    def get_slave_ip(self, slave_id):
        return self.config_data['slaves'][int(slave_id)]['ip']

    def get_slave_port(self, slave_id):
        return self.config_data['slaves'][int(slave_id)]['port']