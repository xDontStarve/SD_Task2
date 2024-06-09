import time, os

from common.grpc_service import GRPCService
from common.config_reader import ConfigReader
from centralized_nodes.master_servicer import MasterServicer
from centralized_nodes.slave_servicer import SlaveServicer
from proto import store_pb2
import threading

from proto.store_pb2 import SlowDownRequest

script_dir = os.path.dirname(os.path.realpath(__file__))

def test():
    slave0Stub = GRPCService.connect("localhost:32771")
    response = slave0Stub.get(store_pb2.GetRequest(key="key"))
    print("get request from slave 0  returns:", response)

def main():
    config_path = os.path.join(script_dir, "eval/centralized_config.yaml")
    configReader = ConfigReader(config_path)
    masterServer, port = GRPCService.listen(configReader.get_master_port(), MasterServicer())
    slave0Server, port = GRPCService.listen(configReader.get_slave_port(0), SlaveServicer("0"))
    slave1Server, port = GRPCService.listen(configReader.get_slave_port(1), SlaveServicer("1"))

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping all nodes")
        masterServer.stop(0)
        slave0Server.stop(0)
        slave1Server.stop(0)

if __name__ == "__main__":
    main()




