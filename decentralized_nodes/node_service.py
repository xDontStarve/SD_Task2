import threading
import time
import uuid

from common.storage_service import StorageService
from common.grpc_service import GRPCService
from common.node_registrator_service import node_registrator
from common.transaction_service import transaction_service
from proto.store_pb2 import *


class NodeService:
    writeVoteCount = 0
    readVoteCount = 0
    readVoteThreshold = 2
    writeVoteThreshold = 3
    def __init__(self, idParameter: str):
        self.id = idParameter
        self.storage = StorageService(f"storage_{self.id}")
        self.writeVoteWeight = 0
        self.readVoteWeight = 0
        self.writeCondition = threading.Condition()
        self.readCondition = threading.Condition()  # Condition variable for synchronization
        match self.id:
            case "0":
                self.writeVoteWeight = 1
                self.readVoteWeight = 1
            case "1":
                self.writeVoteWeight = 2
                self.readVoteWeight = 2
            case "2":
                self.writeVoteWeight = 1
                self.readVoteWeight = 1

    def put(self, key: str, value: str, delay: int) -> bool:
        time.sleep(delay)
        self.writeVoteCount = self.writeVoteWeight
        threads = []
        match self.id:
            case "0":
                node1 = node_registrator.get_node_by_id("1")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node1.ip, node1.port)))
                node2 = node_registrator.get_node_by_id("2")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node2.ip, node2.port)))
            case "1":
                node0 = node_registrator.get_node_by_id("0")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node0.ip, node0.port)))
                node2 = node_registrator.get_node_by_id("2")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node2.ip, node2.port)))
            case"2":
                node0 = node_registrator.get_node_by_id("0")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node0.ip, node0.port)))
                node1 = node_registrator.get_node_by_id("1")
                threads.append(threading.Thread(target=self.askWriteVotes, args=(key, node1.ip, node1.port)))

        for thread in threads:
            thread.start()
        # Wait for the write vote count to reach the threshold
        with self.writeCondition:
            while self.writeVoteCount < self.writeVoteThreshold:
                self.writeCondition.wait()  # Wait for the condition to be notified

        # Check if the threshold is met and proceed
        if self.writeVoteCount >= self.writeVoteThreshold:
            self.storage.add_pair(key, value, self.id)

        # Clean up: Since we do not want to wait for other threads if they are still processing, we will leave them
        # as zombies, therefore we won't do a thread.join() for all threads
        for thread in threads:
            thread.join(timeout=0)

        # Commit in other nodes
        for node in node_registrator.get_all_nodes():
            node_socket = f"{node.ip}:{node.port}"
            client = GRPCService.connect(node_socket)
            client.doCommit(DoCommitRequest(key=key, value=value))
        return True

    def get(self, key: str, delay: int) -> GetResponse:
        self.readVoteCount = self.readVoteWeight
        time.sleep(delay)
        threads = []
        match self.id:
            case "0":
                node1 = node_registrator.get_node_by_id("1")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node1.ip, node1.port)))
                node2 = node_registrator.get_node_by_id("2")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node2.ip, node2.port)))
            case "1":
                node0 = node_registrator.get_node_by_id("0")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node0.ip, node0.port)))
                node2 = node_registrator.get_node_by_id("2")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node2.ip, node2.port)))
            case "2":
                node0 = node_registrator.get_node_by_id("0")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node0.ip, node0.port)))
                node1 = node_registrator.get_node_by_id("1")
                threads.append(threading.Thread(target=self.askReadVotes, args=(key, node1.ip, node1.port)))

        for thread in threads:
            thread.start()
        # Wait for the write vote count to reach the threshold
        with self.readCondition:
            while self.readVoteCount < self.readVoteThreshold:
                self.readCondition.wait()  # Wait for the condition to be notified

        # Check if the threshold is met and proceed
        if self.readVoteCount >= self.readVoteThreshold:
            if self.storage.get_value(key) is None:
                return GetResponse(value=None, found=False)
            else:
                return GetResponse(value=self.storage.get_value(key), found=True)
        # Clean up: Since we do not want to wait for other threads if they are still processing, we will leave them
        # as zombies, therefore we won't do a thread.join() for all threads
        for thread in threads:
            thread.join(timeout=0)

    def doCommit(self, key: str, value: str, delay: int) -> CommitResponse:
        time.sleep(delay)
        self.storage.add_pair(key, value, self.id)
        return CommitResponse(success=True)

    def registerNode(self, node_id: str, ip: str, port: int) -> None:
        node_registrator.add_node(node_id, ip, port)

    def readVote(self, key: str) -> (int, str):
        if (self.storage.get_value(key) is None):
            return 0, None
        else:
            return self.readVoteWeight, self.storage.get_value(key)

    def writeVote(self) -> int:
        return self.writeVoteWeight

    def askWriteVotes(self, key: str, ip: str, port: str):
        print(f"[NODE,", self.id,"] connecting to --> {ip}:{port} to ask for write vote")
        nodeStub = GRPCService.connect(f"{ip}:{port}")
        writeVoteResponse = nodeStub.writeVote(WriteVoteRequest(key=key))
        with self.writeCondition:
            self.writeVoteCount += writeVoteResponse.vote
            self.writeCondition.notify()  # Notify waiting threads that the vote count has changed


    # Return the value of the ReadResponse if necessary (to check that the voter has the same value as the node that requested it)
    def askReadVotes(self, key: str, ip: str, port: str):
        print("[NODE,", self.id, f"] connecting to --> {ip}:{port} to ask for read vote")
        nodeStub = GRPCService.connect(f"{ip}:{port}")
        readVoteResponse = nodeStub.readVote(ReadVoteRequest(key=key))
        with self.readCondition:
            self.readVoteCount += readVoteResponse.vote
            self.readCondition.notify()
