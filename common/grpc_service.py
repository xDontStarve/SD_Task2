from concurrent import futures
import grpc
import proto.store_pb2_grpc as RPC



class GRPCService:
    @staticmethod
    def listen(port: int, servicer) -> any:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        RPC.add_KeyValueStoreServicer_to_server(servicer, server)
        port = server.add_insecure_port(f'0.0.0.0:{port}')
        server.start()
        return server, port

    @staticmethod
    def connect(socket):
        channel = grpc.insecure_channel(f'{socket}')
        stub = RPC.KeyValueStoreStub(channel)
        return stub

