import socket
from typing import List
import subprocess

def client_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port

    host = socket.gethostbyname(socket.gethostname()) # Initiate connection to server
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    
    identification_data = "slave"
    client_socket.send(identification_data.encode()) # Send initial identifer

    print("Connected to server. Awaiting assignment to master server ...")

    # Maintain connection till Server sends Master Node IP
    while True:
        data: List[str] = client_socket.recv(1024).decode().split(";")
        ip: str = data[1]
        port: str = '8786' # data[2]

        print(f"Server assigned us to {ip}:{port}.")
        print(f"Connecting to assigned address ...")
        subprocess.run(["dask", "worker", f"{ip}:{port}"]) 
        break
    
    client_socket.close() # close the connection
    return data

if __name__ == '__main__':
    master_ip = client_program()