import uuid

from common.storage_service import StorageService
from common.grpc_service import GRPCService
from common.node_registrator_service import node_registrator
from common.transaction_service import transaction_service
from proto.store_pb2 import *


class NodeService:

    def __init__(self, id:str):
        self.storage = StorageService(f"storage_{id}")

    def put(self, key: str, value: str) -> bool:
        transactionIdList = {}
        transactionId = str(uuid.uuid4())
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            response = client.prepare(PrepareRequest(transactionId=transactionId, key=key, value=value))
            transactionIdList[node_socket] = response.transactionId
            print("[Master] Node", node.node_id, ". Vote: ", response.voteCommit, "For transaction: ", transactionIdList[node_socket])
            if response.voteCommit == False:
                return False
        self.storage.add_pair(key, value)
        # Commit in other nodes
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            commitResponse = client.commit(CommitRequest(transactionId=transactionIdList[node_socket]))
            if (commitResponse.success == False):
                return False
            print("[Master] Node ", node.node_id, "Committed successfully the transaction: ", transactionIdList[node_socket])
        return True

    def get(self, key: str) -> GetResponse:
        if (self.storage.get_value(key) is None):
            return GetResponse(value=self.storage.get_value(key), found=False)
        return GetResponse(value=self.storage.get_value(key), found=True)

    def prepare(self, transactionId: str, key: str, value: str) -> PrepareResponse:
        transaction_service.store_value(transactionId, key, value)
        return PrepareResponse(transactionId=transactionId, voteCommit=True)

    def commit(self, transactionId: str) -> CommitResponse:
        (key, value) = transaction_service.get_value(transactionId)
        if (key == None or value == None):
            return CommitResponse(success=False)
        self.storage.add_pair(key, value)
        return CommitResponse(success=True)

    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        node_registrator.add_node(node_id, ip, port)
