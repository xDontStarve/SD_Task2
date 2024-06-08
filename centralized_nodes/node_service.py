import uuid

from common.storage_service import StorageService
from common.grpc_service import GRPCService
from common.node_registrator_service import node_registrator
from common.transaction_service import transaction_service
from proto.store_pb2 import *

class NodeService:

    def __init__(self):
        self.storage = StorageService()

    def put(self, key: str, value: str) -> bool:
        transactionIdList = {}
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            transactionId, vote = client.prepare(PrepareRequest(transactionId=str(uuid.uuid4()), key=key, value=value))
            transactionIdList[node_socket] = transactionId
            if vote == False:
                return False
        self.storage.add_pair(key, value)
        # Commit in other nodes
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            client.commit(CommitRequest(transactionId=transactionIdList[node_socket]))

        return True

    def get(self, key: str) -> GetResponse:
        return GetResponse(value=self.storage.get_value(key), found=True)

    def prepare(self, transactionId: str, key: str, value: str) -> (str, bool):
        transaction_service.store_value(transactionId, key, value)
        return transactionId, True

    def commit(self, transactionId: str) -> None:
        (key, value) = transaction_service.get_value(transactionId)
        self.storage.add_pair(key, value)

    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        node_registrator.add_node(node_id, ip, port)
