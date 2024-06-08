class Node:
    def __init__(self, node_id: str, ip: str, port: int):
        self.node_id = node_id
        self.ip = ip
        self.port = port

class NodeRegistrator:
    def __init__(self):
        self.nodes = []  # Initializing an empty list to store nodes

    def add_node(self, node_id: str, ip: str, port: int):
        node = Node(node_id, ip, port)
        self.nodes.append(node)  # Adding a new node to the list

    def get_all_nodes(self):
        return self.nodes  # Returning the list of all nodes

node_registrator = NodeRegistrator()