import time, os

from common.grpc_service import GRPCService
from common.config_reader import ConfigReader
from decentralized_nodes.node_servicer import NodeServicer
from proto import store_pb2
import threading

from proto.store_pb2 import SlowDownRequest, NodeInfo, PutRequest, GetRequest

script_dir = os.path.dirname(os.path.realpath(__file__))

def main():
    config_path = os.path.join(script_dir, "eval/decentralized_config.yaml")
    configReader = ConfigReader(config_path)
    node0Server, port = GRPCService.listen(configReader.get_node0_port(), NodeServicer("0"))
    node1Server, port = GRPCService.listen(configReader.get_node1_port(), NodeServicer("1"))
    node2Server, port = GRPCService.listen(configReader.get_node2_port(), NodeServicer("2"))

    node0Stub = GRPCService.connect(f"{configReader.get_node0_ip()}:{configReader.get_node0_port()}")
    node1Stub = GRPCService.connect(f"{configReader.get_node1_ip()}:{configReader.get_node1_port()}")
    node2Stub = GRPCService.connect(f"{configReader.get_node2_ip()}:{configReader.get_node2_port()}")

    node0Stub.registerSelfToOtherNodes(NodeInfo(node_id="0", ip=configReader.get_node0_ip(), port=configReader.get_node0_port()))
    node1Stub.registerSelfToOtherNodes(NodeInfo(node_id="1", ip=configReader.get_node1_ip(), port=configReader.get_node1_port()))
    node2Stub.registerSelfToOtherNodes(NodeInfo(node_id="2", ip=configReader.get_node2_ip(), port=configReader.get_node2_port()))

    print("\n************* | Initialization finished | *************\n")

    #print(node0Stub.put(PutRequest(key="key", value="value")))
    #print(node1Stub.get(GetRequest(key="key")))


    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping all nodes")
        node0Server.stop(0)
        node1Server.stop(0)
        node2Server.stop(0)

if __name__ == "__main__":
    main()




