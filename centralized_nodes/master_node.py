import time
import uuid

import proto.store_pb2_grpc as RPC
from common.storage_service import storage
from common.node_registrator_service import node_registrator
from common.grpc_service import GRPCService
from common.transaction_service import transaction_service
from proto.store_pb2 import *
from common.config_reader import ConfigReader
import yaml


class MasterServicer(RPC.KeyValueStoreServicer):
    delay = 0

    # Real response should be created in the service, here we create the response
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        print("Put received by the master node, with delay", self.delay, ". Key: ", request.key, " value: ",
              request.value)
        time.sleep(self.delay)
        return PutResponse(NodeService.put(request.key, request.value))

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        print("Get received by the master node, with delay", self.delay, ". Key: ", request.key)
        time.sleep(self.delay)
        return GetResponse(NodeService.get(request.key))

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        print("Slow down request received by the master node, delay: ", request.seconds)
        self.delay = request.seconds
        return SlowDownResponse(True)

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        print("Restore request received by the master node")
        self.delay = 0
        return RestoreResponse(True)

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        print("[Error] Master node does not accept prepare requests")
        # return PrepareResponse(NodeService.prepare(request.transactionId, request.key, request.value))
        pass

    def commit(self, request: CommitRequest, context, **kwargs) -> None:
        print("[Error] Master node does not accept commit requests")
        # NodeService.commit(request.transactionId)
        pass

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> None:
        print("Node registration received by the master node, ip: ", nodeInfo.ip, " Port: ", nodeInfo.port)
        time.sleep(self.delay)
        NodeService.registerNode(nodeInfo.node_id, nodeInfo.ip, nodeInfo.port)


class SlaveServicer(RPC.KeyValueStoreServicer):
    delay = 0

    def __init__(self):
        configReader = ConfigReader("centralized_config.yaml")
        master = GRPCService.connect(f"{configReader.get_master_ip()}:{configReader.get_master_port()}")
        master.registerNode(NodeInfo(configReader.get_slave_ip(0), configReader.get_slave_port(0)))
        master.registerNode(NodeInfo(configReader.get_slave_ip(1), configReader.get_slave_port(1)))

    # Real response should be created in the service, here we create the response
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        print("[Error] slave node does not accept put requests")
        return PutResponse(False)

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        print("Get received by the slave node, with delay", self.delay, ". Key: ", request.key)
        time.sleep(self.delay)
        return GetResponse(NodeService.get(request.key))

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        print("Slow down request received by the slave node, delay: ", request.seconds)
        self.delay = request.seconds
        return SlowDownResponse(True)

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        print("Restore request received by the slave node")
        self.delay = 0
        return RestoreResponse(True)

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        print("Prepare request received by slave node with delay", self.delay, ", transactionID: ", request.transactionId)
        time.sleep(self.delay)
        return PrepareResponse(NodeService.prepare(request.transactionId, request.key, request.value))


    def commit(self, request: CommitRequest, context, **kwargs) -> None:
        print("Commit request received bt the slave node with delay", self.delay, ", transactionID: ", request.transactionId)
        time.sleep(self.delay)
        NodeService.commit(request.transactionId)

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> None:
        print("[Error] Slave node does not accept registerNode requests")
        pass


class NodeService:

    @staticmethod
    def put(self, key: str, value: str) -> bool:
        transactionIdList = {}
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            transactionId, vote = client.prepare(PrepareRequest(str(uuid.uuid4()), key, value))
            transactionIdList[node_socket] = transactionId
            if vote == False:
                return False
        storage.add_pair(key, value)
        # Commit in other nodes
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            client.commit(CommitRequest(transactionIdList[node_socket]))

        return True

    @staticmethod
    def get(self, key: str) -> (str, bool):
        return storage.get_value(key), True

    @staticmethod
    def prepare(self, transactionId: str, key: str, value: str) -> (str, bool):
        transaction_service.store_value(transactionId, key, value)
        return transactionId, True

    @staticmethod
    def commit(self, transactionId: str) -> None:
        (key, value) = transaction_service.get_value(transactionId)
        storage.add_pair(key, value)

    @staticmethod
    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        node_registrator.add_node(node_id, ip, port)
