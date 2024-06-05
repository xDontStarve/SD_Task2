from asyncio import futures


def main():

    pass




if __name__ == "__main__":
    main()




class GRPCService:

    @staticmethod
    def listen(port: int) -> any:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=config_service.get("MAX_WORKERS")))
        RPC.add_PrivateChatServiceServicer_to_server(_PrivateChatServicer(), server)
        port = server.add_insecure_port(f'0.0.0.0:{port}')
        server.start()
        return server, port

    @staticmethod
    def connect(socket):
        channel = grpc.insecure_channel(f'{socket}')
        stub = RPC.PrivateChatServiceStub(channel)
        return stub