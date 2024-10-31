import argparse
import asyncio
import socket
import threading
from time import sleep
from typing import List
from distributed import Worker, WorkerPlugin

client_host = "0.0.0.0"
send_port = 51591
receive_port = 51592

# Custom worker plugin to disconnect worker when task is complete
class DisconnectOnTaskComplete(WorkerPlugin):
    def __init__(self, client):
        self.client = client

    def transition(self, key, start, finish, *args, **kwargs):
        # Check if the transition is to 'finished' state
        if finish == 'memory':
            exit()

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
            worker.plugins['disconnect'] = DisconnectOnTaskComplete(worker)
            await worker.start()
            await worker.finished()
            break
        elif action == 'connect_storage':
            client_socket.send("start_storage_node".encode())
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
    master_key_result = conn.recv(1024).decode()
    parameters = master_key_result.split(";")
    ip = conn.getsockname()[0]
    port = conn.getsockname()[1]
    master = parameters[0]
    key = parameters[1]
    result = parameters[2]

    # Save client IP to text file
    print(f"New result from {ip}:{port} -> {master}'s {key} score {result}.")

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port number')
    args = parser.parse_args()
    
    asyncio.run(client_program(args.ip, args.port))