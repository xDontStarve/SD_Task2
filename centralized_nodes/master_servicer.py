import time

import proto.store_pb2_grpc as RPC
from centralized_nodes.node_service import NodeService
from proto.store_pb2 import *


class MasterServicer(RPC.KeyValueStoreServicer):
    def __init__(self):
        self.delay = 0
        self.nodeService = NodeService("master")
        print("[MASTER]initialize master")

    # Real response should be created in the service, here we create the response
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        print("[MASTER]Put received by the master node, with delay", self.delay, ". Key: ", request.key, " value: ",
              request.value)
        time.sleep(self.delay)
        return PutResponse(success=self.nodeService.put(request.key, request.value))

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        print("[MASTER]Get received by the master node, with delay", self.delay, ". Key: ", request.key)
        time.sleep(self.delay)
        return self.nodeService.get(request.key)

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        print("[MASTER]Slow down request received by the master node, delay: ", request.seconds)
        self.delay = request.seconds
        return SlowDownResponse(success=True)

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        print("[MASTER]Restore request received by the master node")
        self.delay = 0
        return RestoreResponse(success=True)

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        print("[MASTER] [Error] Master node does not accept prepare requests")
        return PrepareResponse(transactionId="", voteCommit=False)

    def commit(self, request: CommitRequest, context, **kwargs) -> Empty:
        print("[MASTER] [Error] Master node does not accept commit requests")
        return Empty()

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> Empty:
        print("[MASTER] Node registration received by the master node, ip: ", nodeInfo.ip, " Port: ", nodeInfo.port)
        time.sleep(self.delay)
        self.nodeService.registerNode(nodeInfo.node_id, nodeInfo.ip, nodeInfo.port)
        return Empty()
