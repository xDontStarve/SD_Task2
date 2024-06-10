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

    def get_node0_ip(self):
        return self.config_data['nodes'][0]['ip']

    def get_node1_ip(self):
        return self.config_data['nodes'][1]['ip']

    def get_node2_ip(self):
        return self.config_data['nodes'][2]['ip']

    def get_node0_port(self):
        return self.config_data['nodes'][0]['port']

    def get_node1_port(self):
        return self.config_data['nodes'][1]['port']

    def get_node2_port(self):
        return self.config_data['nodes'][2]['port']