import os

import proto.store_pb2_grpc as RPC
from centralized_nodes.node_service import NodeService
from common.config_reader import ConfigReader
from common.grpc_service import GRPCService
from proto.store_pb2 import *

script_dir = os.path.dirname(os.path.realpath(__file__))
class SlaveServicer(RPC.KeyValueStoreServicer):
    delay = 0

    def __init__(self, id: str):
        print("[NODE] Initializing slave ", id)
        self.id = id
        config_path = os.path.join(script_dir, "../eval/centralized_config.yaml")
        configReader = ConfigReader(config_path)
        master = GRPCService.connect(f"{configReader.get_master_ip()}:{configReader.get_master_port()}")
        master.registerNode(NodeInfo(node_id=id, ip=configReader.get_slave_ip(id), port=int(configReader.get_slave_port(id))))
        self.nodeService = NodeService(id)

    # Real response should be created in the service, here we create the response
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        print("[NODE] [Error] slave node", self.id, " does not accept put requests")
        return PutResponse(success=False)

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        print("[NODE] Get received by the slave node, with delay", self.delay, ". Key: ", request.key)
        return self.nodeService.get(request.key, self.delay)

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        print("[NODE] Slow down request received by the slave node", self.id, ", delay: ", request.seconds)
        self.delay = request.seconds
        return SlowDownResponse(success=True)

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        print("[NODE] Restore request received by the slave node", self.id)
        self.delay = 0
        return RestoreResponse(success=True)

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        print("[NODE] Prepare request received by slave node", self.id, " with delay", self.delay, ", transactionID: ",
              request.transactionId, "Key: ", request.key, " Value: ", request.value)
        return self.nodeService.prepare(request.transactionId, request.key, request.value, self.delay)

    def commit(self, request: CommitRequest, context, **kwargs) -> CommitResponse:
        print("[NODE] Commit request received bt the slave node", self.id, " with delay", self.delay, ", transactionID: ",
              request.transactionId)
        return self.nodeService.commit(request.transactionId, self.delay)

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> Empty:
        print("[NODE] [Error] Slave node", self.id, " does not accept registerNode requests")
        return Empty()

    def doCommit(self, request: DoCommitRequest, context, **kwargs) -> Empty:
        print("[NODE] Slave node received doCommit request for value:", request.value, "value:", request.value)
        self.nodeService.doCommit(request.key, request.value)
        return Empty()