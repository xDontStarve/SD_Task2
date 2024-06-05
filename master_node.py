import proto.store_pb2_grpc as RPC
from proto.store_pb2 import *


class MasterServicer(RPC.KeyValueStoreServicer):
    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        # TODO: Return response object, real response should be created in the service
        return PutResponse(MasterService.put(request.key, request.value))

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        pass

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        pass

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        pass

    def prepare(self, request: PrepareRequest, context, **kwargs) -> PrepareResponse:
        pass

    def commit(self, request: CommitRequest, context, **kwargs) -> CommitResponse:
        pass

    def abort(self, request: AbortRequest, context, **kwargs) -> AbortResponse:
        pass

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> NodeRegisterResponse:
        pass

class MasterService:
    @staticmethod
    def put(self, key: str, value: str) -> bool:
        # TODO: Here we calculate the result (bool)
        # TODO: Method logic
        ...

    @staticmethod
    def get(self, request: GetRequest) -> GetResponse:
        pass

    @staticmethod
    def slowDown(self, request: SlowDownRequest) -> SlowDownResponse:
        pass

    @staticmethod
    def restore(self, request: RestoreRequest) -> RestoreResponse:
        pass

    @staticmethod
    def prepare(self, request: PrepareRequest) -> PrepareResponse:
        pass

    @staticmethod
    def commit(self, request: CommitRequest) -> CommitResponse:
        pass

    @staticmethod
    def abort(self, request: AbortRequest) -> AbortResponse:
        pass

    @staticmethod
    def registerNode(self, nodeInfo: NodeInfo) -> NodeRegisterResponse:
        pass