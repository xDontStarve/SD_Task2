# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import store_pb2 as store__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in store_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class KeyValueStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.put = channel.unary_unary(
                '/distributedstore.KeyValueStore/put',
                request_serializer=store__pb2.PutRequest.SerializeToString,
                response_deserializer=store__pb2.PutResponse.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/distributedstore.KeyValueStore/get',
                request_serializer=store__pb2.GetRequest.SerializeToString,
                response_deserializer=store__pb2.GetResponse.FromString,
                _registered_method=True)
        self.slowDown = channel.unary_unary(
                '/distributedstore.KeyValueStore/slowDown',
                request_serializer=store__pb2.SlowDownRequest.SerializeToString,
                response_deserializer=store__pb2.SlowDownResponse.FromString,
                _registered_method=True)
        self.restore = channel.unary_unary(
                '/distributedstore.KeyValueStore/restore',
                request_serializer=store__pb2.RestoreRequest.SerializeToString,
                response_deserializer=store__pb2.RestoreResponse.FromString,
                _registered_method=True)
        self.prepare = channel.unary_unary(
                '/distributedstore.KeyValueStore/prepare',
                request_serializer=store__pb2.PrepareRequest.SerializeToString,
                response_deserializer=store__pb2.PrepareResponse.FromString,
                _registered_method=True)
        self.commit = channel.unary_unary(
                '/distributedstore.KeyValueStore/commit',
                request_serializer=store__pb2.CommitRequest.SerializeToString,
                response_deserializer=store__pb2.Empty.FromString,
                _registered_method=True)
        self.registerNode = channel.unary_unary(
                '/distributedstore.KeyValueStore/registerNode',
                request_serializer=store__pb2.NodeInfo.SerializeToString,
                response_deserializer=store__pb2.Empty.FromString,
                _registered_method=True)


class KeyValueStoreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def slowDown(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def restore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def prepare(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def commit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def registerNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeyValueStoreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'put': grpc.unary_unary_rpc_method_handler(
                    servicer.put,
                    request_deserializer=store__pb2.PutRequest.FromString,
                    response_serializer=store__pb2.PutResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=store__pb2.GetRequest.FromString,
                    response_serializer=store__pb2.GetResponse.SerializeToString,
            ),
            'slowDown': grpc.unary_unary_rpc_method_handler(
                    servicer.slowDown,
                    request_deserializer=store__pb2.SlowDownRequest.FromString,
                    response_serializer=store__pb2.SlowDownResponse.SerializeToString,
            ),
            'restore': grpc.unary_unary_rpc_method_handler(
                    servicer.restore,
                    request_deserializer=store__pb2.RestoreRequest.FromString,
                    response_serializer=store__pb2.RestoreResponse.SerializeToString,
            ),
            'prepare': grpc.unary_unary_rpc_method_handler(
                    servicer.prepare,
                    request_deserializer=store__pb2.PrepareRequest.FromString,
                    response_serializer=store__pb2.PrepareResponse.SerializeToString,
            ),
            'commit': grpc.unary_unary_rpc_method_handler(
                    servicer.commit,
                    request_deserializer=store__pb2.CommitRequest.FromString,
                    response_serializer=store__pb2.Empty.SerializeToString,
            ),
            'registerNode': grpc.unary_unary_rpc_method_handler(
                    servicer.registerNode,
                    request_deserializer=store__pb2.NodeInfo.FromString,
                    response_serializer=store__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'distributedstore.KeyValueStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('distributedstore.KeyValueStore', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class KeyValueStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/put',
            store__pb2.PutRequest.SerializeToString,
            store__pb2.PutResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/get',
            store__pb2.GetRequest.SerializeToString,
            store__pb2.GetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def slowDown(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/slowDown',
            store__pb2.SlowDownRequest.SerializeToString,
            store__pb2.SlowDownResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def restore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/restore',
            store__pb2.RestoreRequest.SerializeToString,
            store__pb2.RestoreResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def prepare(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/prepare',
            store__pb2.PrepareRequest.SerializeToString,
            store__pb2.PrepareResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def commit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/commit',
            store__pb2.CommitRequest.SerializeToString,
            store__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def registerNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distributedstore.KeyValueStore/registerNode',
            store__pb2.NodeInfo.SerializeToString,
            store__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
