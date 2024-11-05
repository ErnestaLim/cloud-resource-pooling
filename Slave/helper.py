# Ask central server for stroage nodes addresses
import argparse
import pickle
import socket


def get_storage_nodes():  
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port number')
    parser.add_argument('--storage_ip', type=str, help='If connected as storage node, provide the IP address of the storage server')
    parser.add_argument('--storage_port', type=int, help='If connected as storage node, provide the port number of the storage server')
    args = parser.parse_args()

    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((args.ip, args.port))

    # Send initial identifer
    message = "get_storage_nodes"
    client_socket.send(message.encode())

    print("Requesting central server for storage nodes' addresses ...")

    # Wait for response (blocking call)
    response = client_socket.recv(4096)
    storage_nodes = pickle.loads(response)

    return storage_nodes