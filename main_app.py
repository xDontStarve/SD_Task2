import threading
import subprocess
import os
import time

from common.config_reader import ConfigReader
from common.grpc_service import GRPCService
from decentralized_nodes.node_servicer import NodeServicer
from proto.store_pb2 import PutRequest, GetRequest

script_dir = os.path.dirname(os.path.realpath(__file__))

def execute_script(script_name):
    subprocess.run(["python", script_name])

def write(choice: int, node: int):
    #Prepare data
    if choice == 1:
        config_path = os.path.join(script_dir, "eval/centralized_config.yaml")
        configReader = ConfigReader(config_path)
        match node:
            case 0:
                stub = GRPCService.connect(f"{configReader.get_master_ip()}:{configReader.get_master_port()}")
            case 1:
                stub = GRPCService.connect(f"{configReader.get_slave_ip(0)}:{configReader.get_slave_port(0)}")
            case 2:
                stub = GRPCService.connect(f"{configReader.get_slave_ip(1)}:{configReader.get_slave_port(1)}")

        user_input = input("Enter the key and value separated by a comma ',' (key,value):")
        values = user_input.split(',')
        key, value = values[0], values[1]
        print("put response:", stub.put(PutRequest(key=key, value=value)))

    elif choice == 2:
        config_path = os.path.join(script_dir, "eval/decentralized_config.yaml")
        configReader = ConfigReader(config_path)
        match node:
            case 0:
                stub = GRPCService.connect(f"{configReader.get_node0_ip()}:{configReader.get_node0_port()}")
            case 1:
                stub = GRPCService.connect(f"{configReader.get_node1_ip()}:{configReader.get_node1_port()}")
            case 2:
                stub = GRPCService.connect(f"{configReader.get_node2_ip()}:{configReader.get_node2_port()}")

        user_input = input("Enter the key and value separated by a comma ',' (key,value):")
        values = user_input.split(',')
        key, value = values[0], values[1]
        print("put response:", stub.put(PutRequest(key=key, value=value)))
    time.sleep(2)

def get(choice: int, node: int):
    # Prepare data
    if choice == 1:
        config_path = os.path.join(script_dir, "eval/centralized_config.yaml")
        configReader = ConfigReader(config_path)
        match node:
            case 0:
                stub = GRPCService.connect(f"{configReader.get_master_ip()}:{configReader.get_master_port()}")
            case 1:
                stub = GRPCService.connect(f"{configReader.get_slave_ip(0)}:{configReader.get_slave_port(0)}")
            case 2:
                stub = GRPCService.connect(f"{configReader.get_slave_ip(1)}:{configReader.get_slave_port(1)}")

        key = input("Enter the key:")
        print("get response:", stub.get(GetRequest(key=key)))

    elif choice == 2:
        config_path = os.path.join(script_dir, "eval/decentralized_config.yaml")
        configReader = ConfigReader(config_path)
        match node:
            case 0:
                stub = GRPCService.connect(f"{configReader.get_node0_ip()}:{configReader.get_node0_port()}")
            case 1:
                stub = GRPCService.connect(f"{configReader.get_node1_ip()}:{configReader.get_node1_port()}")
            case 2:
                stub = GRPCService.connect(f"{configReader.get_node2_ip()}:{configReader.get_node2_port()}")

        key = input("Enter the key:")
        print("get response:", stub.get(GetRequest(key=key)))
    time.sleep(2)

def main():
    global thread
    while True:
        print("Do you want to use the centralized or decentralized version?")
        print("1. Centralized")
        print("2. Decentralized")
        print("3. Exit")
        # Choice 1 = centralized
        # Choice 2 = decentralized
        choice = input("Enter your choice: ")

        if choice == "1":
            thread = threading.Thread(target=execute_script, args=("centralized.py",))
            thread.start()
        elif choice == "2":
            thread = threading.Thread(target=execute_script, args=("decentralized.py",))
            thread.start()
        elif choice == "3":
            print("OK ending nodes thread...")
            thread.join(timeout=0)
            break
        else:
            print("Invalid choice. Please try again.")
        time.sleep(2)

        while True:
            print("\n\n--------------------------------------------------------------------\nChoose one of the three nodes: 0 (master in centralized), 1 or 2")
            print("To exit, enter 3")
            option = input("Enter your option: ")

            if option in ["0", "1", "2"]:
                print("1. Put")
                print("2. Get")
                print("3. Exit")
                action = input("Enter your action: ")

                if action == "1":
                    write(int(choice), int(option))
                elif action == "2":
                    get(int(choice), int(option))
                else:
                    print("Invalid action. Please try again.")
            elif option == "3":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()