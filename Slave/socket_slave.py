import argparse
import asyncio
import socket
import threading
from typing import List
from distributed import Worker

async def client_program(host: str, port: int): 
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    
    client_ip, client_port = client_socket.getsockname()
    identification_data = "slave"
    client_socket.send(identification_data.encode()) # Send initial identifer

    print(f"Connected to server as {client_ip}:{client_port}. Awaiting assignment to master server ...")

    # Maintain connection till Server sends Master Node IP
    while True:
        data: List[str] = client_socket.recv(1024).decode().split(";")
        action = data[0]

        # Close connection to central server
        client_socket.close()

        if action == 'connect':
            ip: str = data[1]
            port: str = '8786' # data[2]

            # Connect as dask worker to assigned master server
            print(f"Server assigned us to {ip}:{port}.")
            print(f"Connecting to assigned address ...")
            worker = Worker(ip, port, host = f"{client_ip}:{client_port}")
            await worker.start()
            await worker.finished()
            break
        elif action == 'connect_storage':
            storage_loop(host=client_ip, port=client_port)
    
    return True

def storage_loop(host, port):
    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(10)
    print(f"Storage server listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept() # Accept new connections
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