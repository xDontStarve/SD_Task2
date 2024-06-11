import os

import proto.store_pb2_grpc as RPC
from decentralized_nodes.node_service import NodeService
from common.config_reader import ConfigReader
from common.grpc_service import GRPCService
from proto.store_pb2 import *

script_dir = os.path.dirname(os.path.realpath(__file__))


class NodeServicer(RPC.KeyValueStoreServicer):
    delay = 0

    def __init__(self, id: str):
        print("[NODE", id, "] Initializing node ", id)
        self.id = id
        self.nodeService = NodeService(id)

    def put(self, request: PutRequest, context, **kwargs) -> PutResponse:
        print("[NODE", self.id, "] Put received by the node, with delay", self.delay, ". Key: ", request.key,
              " value: ",
              request.value)
        return PutResponse(success=self.nodeService.put(request.key, request.value, self.delay))

    def get(self, request: GetRequest, context, **kwargs) -> GetResponse:
        print("[NODE", self.id, "] Get received by the node, with delay", self.delay, ". Key: ", request.key)
        return self.nodeService.get(request.key, self.delay)

    def slowDown(self, request: SlowDownRequest, context, **kwargs) -> SlowDownResponse:
        print("[NODE", self.id, "] Slow down request received by the node", self.id, ", delay: ", request.seconds)
        self.delay = request.seconds
        return SlowDownResponse(success=True)

    def restore(self, request: RestoreRequest, context, **kwargs) -> RestoreResponse:
        print("[NODE", self.id, "] Restore request received by the node", self.id)
        self.delay = 0
        return RestoreResponse(success=True)

    def commit(self, request: CommitRequest, context, **kwargs) -> CommitResponse:
        print("[NODE", self.id, "] Commit request received bt the node", self.id, " with delay", self.delay,
              ", transactionID: ",
              request.transactionId)
        return self.nodeService.commit(request.transactionId, self.delay)

    def registerNode(self, nodeInfo: NodeInfo, context, **kwargs) -> Empty:
        print("[NODE", self.id, "] Node registration received. ip: ", nodeInfo.ip, " Port: ",
              nodeInfo.port)
        self.nodeService.registerNode(nodeInfo.node_id, nodeInfo.ip, nodeInfo.port)
        return Empty()

    def readVote(self, request: ReadVoteRequest, context, **kwargs) -> ReadVoteResponse:
        (vote, value) = self.nodeService.readVote(request.key, self.id)
        return ReadVoteResponse(vote=vote, value=value)

    def writeVote(self, request: WriteVoteRequest, context, **kwargs) -> WriteVoteResponse:
        return WriteVoteResponse(vote=self.nodeService.writeVote(request.key, self.id))

    def registerSelfToOtherNodes(self, nodeInfo: NodeInfo, context, **kwargs) -> Empty:
        config_path = os.path.join(script_dir, "../eval/decentralized_config.yaml")
        configReader = ConfigReader(config_path)
        # Register the node for the other two nodes
        match nodeInfo.node_id:
            case "0":
                nodeAStub = GRPCService.connect(f"{configReader.get_node1_ip()}:{configReader.get_node1_port()}")
                nodeBStub = GRPCService.connect(f"{configReader.get_node2_ip()}:{configReader.get_node2_port()}")
                nodeAStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node0_ip(), port=configReader.get_node0_port()))
                print("Node", id, "registered to node 1")
                nodeBStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node0_ip(), port=configReader.get_node0_port()))
                print("Node", id, "registered to node 2")
                pass
            case "1":
                nodeAStub = GRPCService.connect(f"{configReader.get_node0_ip()}:{configReader.get_node0_port()}")
                nodeBStub = GRPCService.connect(f"{configReader.get_node2_ip()}:{configReader.get_node2_port()}")
                nodeAStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node1_ip(), port=configReader.get_node1_port()))
                print("Node", id, "registered to node 0")
                nodeBStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node1_ip(), port=configReader.get_node1_port()))
                print("Node", id, "registered to node 2")
                pass
            case "2":
                nodeAStub = GRPCService.connect(f"{configReader.get_node0_ip()}:{configReader.get_node0_port()}")
                nodeBStub = GRPCService.connect(f"{configReader.get_node1_ip()}:{configReader.get_node1_port()}")
                nodeAStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node2_ip(), port=configReader.get_node2_port()))
                print("Node", id, "registered to node 0")
                nodeBStub.registerNode(
                    NodeInfo(node_id=self.id, ip=configReader.get_node2_ip(), port=configReader.get_node2_port()))
                print("Node", id, "registered to node 1")
                pass
        return Empty()