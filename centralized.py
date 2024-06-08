import time

from common.grpc_service import GRPCService
from common.config_reader import ConfigReader
from centralized_nodes.master_slave import MasterServicer
from centralized_nodes.slave_servicer import SlaveServicer

def main():

    configReader = ConfigReader("centralized_config.yaml")
    masterServer, port = GRPCService.listen(configReader.get_master_port(), MasterServicer())
    time.sleep(1)
    slave0Server, port = GRPCService.listen(configReader.get_slave_port(0), SlaveServicer("0"))
    slave1Server, port = GRPCService.listen(configReader.get_slave_port(1), SlaveServicer("1"))

    masterServer.stop(0)
    slave0Server.stop(0)
    slave1Server.stop(0)

    while (True):
        pass




if __name__ == "__main__":
    main()




