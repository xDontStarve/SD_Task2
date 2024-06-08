import time, os

from common.grpc_service import GRPCService
from common.config_reader import ConfigReader
from centralized_nodes.master_servicer import MasterServicer
from centralized_nodes.slave_servicer import SlaveServicer
from proto import store_pb2


def main():

    configReader = ConfigReader("centralized_config.yaml")
    masterServer, port = GRPCService.listen(configReader.get_master_port(), MasterServicer())
    time.sleep(1)
    slave0Server, port = GRPCService.listen(configReader.get_slave_port(0), SlaveServicer("0"))
    slave1Server, port = GRPCService.listen(configReader.get_slave_port(1), SlaveServicer("1"))

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        masterStub = GRPCService.connect("localhost:32770")
        putResponse = masterStub.put(store_pb2.PutRequest(key="key", value="value"))
        slave0Stub = GRPCService.connect("localhost:32771")
        slave0Stub.put(store_pb2.PutRequest(key="key", value="value"))
        response = slave0Stub.get(store_pb2.GetRequest(key="key"))
        print("get request from slave 0  returns:", response)
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping servers")
        masterServer.stop(0)
        slave0Server.stop(0)
        slave1Server.stop(0)

if __name__ == "__main__":
    main()




