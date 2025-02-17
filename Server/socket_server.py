import json
import os
import pickle
import socket
import threading
import time
from typing import List

import mysql
from  send_email import send_email
from const import MINIMUM_STORAGE_NODES, slave_nodes, master_nodes
from storage_factory import save_storage_node, storage_nodes, storage_update

db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'host': os.getenv('DB_HOST', '127.0.0.1:3306'),
    'database': os.getenv('DB_NAME', 'cloud')
}

def handle_client(conn: socket.socket, address: tuple):
    client_type = conn.recv(1024).decode()
    # Save client IP to text file
    print(f"Connection from {client_type} : {address}")

    if client_type == 'slave':
        slave_process(conn, address)
    elif client_type == 'master':
        send_email()
        master_process(conn, address)
    elif client_type == 'get_storage_nodes':
        conn.sendall(pickle.dumps(storage_nodes))
    else:
        conn.close()

def slave_process(conn: socket.socket, address: tuple):
    global slave_nodes, master_nodes

    # If there is no X storage nodes, we assign them as dedicated storage node
    if len(storage_nodes) < MINIMUM_STORAGE_NODES:
        print(f"Requesting {address[0]} to be a storage node.")

        # If there is an existing storage node, add the IP as parameter, so the new storage node can duplicate the data
        if len(storage_nodes) > 0:
            conn.sendall(f"connect_storage;{storage_nodes[0][0]};{storage_nodes[0][1]}".encode())
        else:
            conn.sendall("connect_storage;".encode())

        while True:
            reply = conn.recv(1024).decode().split(";")
            action = reply[0]

            if action == "start_storage_node":
                storage_ip = reply[1]
                storage_port = reply[2]
                storage_nodes.append((storage_ip, int(storage_port)))
                print(f"Storage {storage_nodes[-1][0]}:{storage_nodes[-1][1]} node connected.")
                save_storage_node(storage_ip, storage_port)
                return
    else:
        slave_nodes.append(conn)
    
    # Wait until master node request for slave node
    while True:
        reply = conn.recv(1024).decode()

        if conn not in slave_nodes:
            conn.sendall("exit;".encode())
            conn.close()
            return

        if not reply:
            print(f"{address[0]}:{address[1]} is down and has been removed from available slave nodes.")
            slave_nodes.remove(conn)
            return
        

def master_process(conn: socket.socket, address: tuple):
    global slave_nodes, master_nodes
    master_nodes.append(master_nodes)
    
    # Wait until master request for slave node(s)
    while True:
        data: List[str] = conn.recv(1024).decode().split(";")
        req_type: str = data[0]
        req_args: List[str] = data[1:]

        if req_type == 'request' or req_type == 'request_storage':
            slave_requested: int = int(req_args[0])
            print(f"{address[0]}:{address[1]} requested for {slave_requested} slaves.")
            print(f"We have {len(slave_nodes)} slave nodes.")

            # Check if we have enough slave
            if len(slave_nodes) < slave_requested:
                response = {
                    "success": False,
                    "message": "Not enough slave nodes."
                }

                conn.sendall(json.dumps(response).encode())
                continue
            else:
                addresses: List[socket.socket] = slave_nodes[:slave_requested]
                slave_nodes = slave_nodes[slave_requested:] # remove slave nodes from list

                # Tell slave node to connect to master node
                for slave_node in addresses:
                    print(f"Assigned {slave_node.getsockname()[0]}:{slave_node.getsockname()[1]} to {address[0]}:{address[1]}.")
                    slave_node.send(f"connect;{address[0]};{address[1]}".encode())
                
                # Send success to master node
                response = {
                    "success": True,
                    "addresses": [address.getpeername() for address in addresses]
                }
                conn.sendall(json.dumps(response).encode())

                continue

def server_program():
    host = socket.gethostbyname(socket.gethostname()) # Get the server hostname or IP
    port = 5000 # Define server port    
    server_socket = socket.socket() # Create socket instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port)) # Bind the server to the host and port

    server_socket.listen(10) # Listen for up to X clients simultaneously
    print(f"Server listening on {host}:{port}")

    # Storage thread
    threading.Thread(target=storage_update).start()

    while True:
        conn, address = server_socket.accept() # Accept new connections
        client_thread = threading.Thread(target=handle_client, args=(conn, address)) # Create a new thread for each client
        client_thread.start()

if __name__ == '__main__':
    server_program()
