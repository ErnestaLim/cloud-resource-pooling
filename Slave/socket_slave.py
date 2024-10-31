import argparse
import asyncio
import pickle
import socket
import threading
from time import sleep
from typing import List
from distributed import Worker, WorkerPlugin

client_host = "0.0.0.0"
send_port = 51591
receive_port = 51592

storage_results = {}

# Custom worker plugin to disconnect worker when task is complete
class DisconnectOnTaskComplete(WorkerPlugin):
    def __init__(self, client):
        self.client = client

    def transition(self, key, start, finish, *args, **kwargs):
        # Check if the transition is to 'finished' state
        # Exit with 1 (error code) so Docker container restarts
        if finish == 'memory':
            exit(1)

async def client_program(host: str, port: int): 
    client_socket = socket.socket() # Initiate connection to server
    client_socket.bind((client_host, send_port))
    client_socket.connect((host, port))
    identification_data = "slave"
    client_socket.send(identification_data.encode()) # Send initial identifer

    print(f"Connected to server as {client_host}:{send_port}. Awaiting assignment to master server ...")

    # Maintain connection till Server sends Master Node IP
    while True:
        data: List[str] = client_socket.recv(1024).decode().split(";")
        action = data[0]

        if action == 'connect':
            ip: str = data[1]
            port: str = '8786' # data[2]

            # Connect as dask worker to assigned master server
            print(f"Server assigned us to {ip}:{port}.")
            print(f"Connecting to assigned address ...")
            worker = Worker(ip, port)
            print("Connecting to master server ...")
            worker.plugins['disconnect'] = DisconnectOnTaskComplete(worker)
            await worker.start()
            print("Connected to master server. Awaiting task ...")
            await worker.finished()
            break
        elif action == 'connect_storage':
            client_socket.send(f"start_storage_node;{receive_port}".encode())
            storage_loop()
    
    return True

def storage_loop():
    storage_socket = socket.socket()
    storage_socket.bind((client_host, receive_port))
    storage_socket.listen(10)
    print(f"Storage server listening on {client_host}:{receive_port}")

    while True:
        conn, address = storage_socket.accept() # Accept new connections
        client_thread = threading.Thread(target=handle_slave, args=(conn, address)) # Create a new thread for each client
        client_thread.start()

def handle_slave(conn, address):
    parameters = conn.recv(1024).decode().split(";")
    action = parameters[0]
    
    if action == "store":
        storage_store(conn, address, parameters)
    elif action == "retrieve":
        storage_retrieve(conn, address, parameters)
    elif action == "delete":
        storage_delete(conn, address, parameters)

def storage_store(conn, address, parameters):
    username = parameters[1]
    llm_name = parameters[2]
    eval_name = parameters[3]
    result = parameters[4]
    
    print(f"New result -> {username} -> {llm_name} -> {eval_name} -> {result}.")

    if username not in storage_results:
        storage_results[username] = {}
    
    if llm_name not in storage_results[username]:
        storage_results[username][llm_name] = {}
    
    storage_results[username][llm_name][eval_name] = result

def storage_retrieve(conn, address, parameters):
    username = parameters[1]
    llm_name = parameters[2]
    
    # Check if the user and llm_name are in storage_results
    if username not in storage_results or llm_name not in storage_results[username]:
        conn.send(pickle.dumps(None))  # Send None if no results are found
        return
    
    # Get the results
    results = storage_results[username][llm_name]
    
    # Pickle the results and send over the connection
    conn.send(pickle.dumps(results))

def storage_delete(conn, address, parameters):
    username = parameters[1]
    llm_name = parameters[2]
    
    # Check if the user and llm_name are in storage_results
    if username not in storage_results or llm_name not in storage_results[username]:
        return
    
    # Delete the results
    del storage_results[username][llm_name]

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port number')
    args = parser.parse_args()
    
    asyncio.run(client_program(args.ip, args.port))