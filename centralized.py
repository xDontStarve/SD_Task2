from asyncio import futures
from master_node import MasterServicer
import grpc
import proto.store_pb2_grpc as RPC


def main():

    pass




if __name__ == "__main__":
    main()




class GRPCService:

    @staticmethod
    def listen(port: int) -> any:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        RPC.add_KeyValueStoreServicer_to_server(MasterServicer(), server)
        port = server.add_insecure_port(f'0.0.0.0:{port}')
        server.start()
        return server, port

    @staticmethod
    def connect(socket):
        channel = grpc.insecure_channel(f'{socket}')
        stub = RPC.PrivateChatServiceStub(channel)
        return stub

