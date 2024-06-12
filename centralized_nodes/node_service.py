import time
import uuid

from common.storage_service import StorageService
from common.grpc_service import GRPCService
from common.node_registrator_service import node_registrator
from common.transaction_service import transaction_service
from proto.store_pb2 import *


class NodeService:

    def __init__(self, idParam:str):
        self.id = idParam
        self.storage = StorageService(f"storage_{self.id}")

    def put(self, key: str, value: str, delay: int) -> bool:
        time.sleep(delay)
        transactionIdList = {}
        transactionId = str(uuid.uuid4())
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            try:
                response = client.prepare(PrepareRequest(transactionId=transactionId, key=key, value=value))
            except Exception as e:
                print("[MASTER] [ERROR] One of the nodes took too long to respond during prepare phase, put operation failed.")
                return False
            transactionIdList[node_socket] = response.transactionId
            print("[Master] Node", node.node_id, ". Vote: ", response.voteCommit, "For transaction: ", transactionIdList[node_socket])
            if not response.voteCommit:
                # If any node returns False, we need to update all nodes to the old value
                for node in node_registrator.get_all_nodes():
                    node_socket = f"{node.ip}:{node.port}"
                    client = GRPCService.connect(node_socket)
                    client.doCommit(DoCommitRequest(key=key, value=value))
                return False
        self.storage.add_pair(key, value, self.id)
        # Commit in other nodes
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            try:
                commitResponse = client.commit(CommitRequest(transactionId=transactionIdList[node_socket]))
            except Exception as e:
                print("[MASTER] One of the nodes took too long to respond during commit phase, put operation failed.")
                return False
            if (commitResponse.success == False):
                # This case shouldn't happen, but if it does, some nodes may already have stored the data.
                return False
            print("[Master] Node ", node.node_id, "Committed successfully the transaction: ", transactionIdList[node_socket])
        return True

    def get(self, key: str, delay: int) -> GetResponse:
        time.sleep(delay)
        if (self.storage.get_value(key) is None):
            return GetResponse(value=self.storage.get_value(key), found=False)
        return GetResponse(value=self.storage.get_value(key), found=True)

    def prepare(self, transactionId: str, key: str, value: str, delay: int) -> PrepareResponse:
        time.sleep(delay)
        transaction_service.store_value(transactionId, key, value)
        self.storage.delete_value(key)
        return PrepareResponse(transactionId=transactionId, voteCommit=True)

    def commit(self, transactionId: str, delay: int) -> CommitResponse:
        time.sleep(delay)
        (key, value) = transaction_service.get_value(transactionId)
        if (key == None or value == None):
            return CommitResponse(success=False)
        self.storage.add_pair(key, value, self.id)
        return CommitResponse(success=True)

    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        node_registrator.add_node(node_id, ip, port)

    def doCommit(self, key: str, value: str):
        self.storage.add_pair(key, value, self.id)
