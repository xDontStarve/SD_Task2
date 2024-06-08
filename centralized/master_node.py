import proto.store_pb2_grpc as RPC
from common.storage_service import storage
from proto.store_pb2 import *


class MasterServicer(RPC.KeyValueStoreServicer):
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        # TODO: Return response object, real response should be created in the service
        return PutResponse(MasterService.put(request.key, request.value))

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        return GetResponse(MasterService.get(request.key))

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        return SlowDownResponse(MasterService.slowDown(request.seconds))

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        return RestoreResponse(MasterService.restore())

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        return PrepareResponse(MasterService.prepare(request.transactionId, request.key, request.value))

    def commit(self, request: CommitRequest, context, **kwargs) -> None:
        MasterService.commit(request.transactionId)

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> None:
        MasterService.registerNode(nodeInfo.node_id, nodeInfo.ip, nodeInfo.port)

class MasterService:

    @staticmethod
    def put(self, key: str, value: str) -> bool:
        # TODO: Here we calculate the result (bool)
        # TODO: Method logic
        ...

    @staticmethod
    def get(self, key: str) -> (str, bool):
        pass

    @staticmethod
    def slowDown(self, seconds: int) -> bool:
        pass

    @staticmethod
    def restore(self) -> bool:
        pass

    @staticmethod
    def prepare(self, transactionId: str, key: str, value:str) -> (str, bool):
        pass

    @staticmethod
    def commit(self, transactionId: str) -> None:
        pass

    @staticmethod
    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        pass
