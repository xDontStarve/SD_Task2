import time, os

from common.grpc_service import GRPCService
from common.config_reader import ConfigReader
from decentralized_nodes.node_servicer import NodeServicer
from proto import store_pb2
import threading

from proto.store_pb2 import SlowDownRequest

script_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    config_path = os.path.join(script_dir, "eval/decentralized_config.yaml")
    configReader = ConfigReader(config_path)
    nose0Server, port = GRPCService.listen(configReader.get_node0_port(), NodeServicer("0"))
    nose1Server, port = GRPCService.listen(configReader.get_node1_port(), NodeServicer("1"))
    nose2Server, port = GRPCService.listen(configReader.get_node2_port(), NodeServicer("2"))

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping all nodes")
        nose0Server.stop(0)
        nose1Server.stop(0)
        nose2Server.stop(0)

if __name__ == "__main__":
    main()




