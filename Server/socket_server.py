import json
import pickle
import socket
import threading
from typing import List
import send_email

slave_nodes: List[socket.socket] = []
master_nodes: List[socket.socket] = []
storage_nodes: List[tuple] = []

def handle_client(conn: socket.socket, address: tuple):
    client_type = conn.recv(1024).decode()
    # Save client IP to text file
    print(f"Connection from {client_type} : {address}")

    if client_type == 'slave':
        slave_process(conn, address)
    elif client_type == 'master':
        master_process(conn, address)
    elif client_type == 'get_storage_nodes':
        conn.sendall(pickle.dumps(storage_nodes))
    else:
        conn.close()

def slave_process(conn: socket.socket, address: tuple):
    global slave_nodes, master_nodes

    # If there is no X storage nodes, we assign them as dedicated storage node
    if len(storage_nodes) < 1:
        print(f"Requesting {address[0]} to be a storage node.")
        conn.sendall("connect_storage;".encode())

        while True:
            reply = conn.recv(1024).decode().split(";")
            action = reply[0]
            storage_port = reply[1]

            if action == "start_storage_node":
                storage_nodes.append((conn.getpeername()[0], int(storage_port)))
                print(f"Storage {storage_nodes[-1][0]}:{storage_nodes[-1][1]} node connected.")
    else:
        slave_nodes.append(conn)
    
    # Wait until master node request for slave node
    while True:
        pass

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
                slave_nodes = slave_nodes[slave_requested:]

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
    server_socket.bind((host, port)) # Bind the server to the host and port

    server_socket.listen(10) # Listen for up to X clients simultaneously
    print(f"Server listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept() # Accept new connections
        client_thread = threading.Thread(target=handle_client, args=(conn, address)) # Create a new thread for each client
        client_thread.start()

if __name__ == '__main__':
    server_program()
