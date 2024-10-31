import argparse
import asyncio
import socket
from typing import List
import subprocess

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
        ip: str = data[1]
        port: str = '8786' # data[2]

        # Close connection to central server
        client_socket.close()

        # Connect as dask worker to assigned master server
        print(f"Server assigned us to {ip}:{port}.")
        print(f"Connecting to assigned address ...")
        worker = Worker(ip, port, host = f"{client_ip}:{client_port}")
        await worker.start()
        await worker.finished()
        break
    
    return data

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port number')
    args = parser.parse_args()
    
    asyncio.run(client_program(args.ip, args.port))