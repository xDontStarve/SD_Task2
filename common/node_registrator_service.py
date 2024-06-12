class Node:
    def __init__(self, node_id: str, ip: str, port: int):
        self.node_id = node_id
        self.ip = ip
        self.port = port

class NodeRegistrator:
    def __init__(self):
        self.nodes = []

    def add_node(self, node_id: str, ip: str, port: int):
        node = Node(node_id, ip, port)
        self.nodes.append(node)

    def get_all_nodes(self):
        return self.nodes

    def get_node_by_id(self, node_id: str):
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None  # Return None if no node matches the given ID

node_registrator = NodeRegistrator()