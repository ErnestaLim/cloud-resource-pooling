import socket
import time
from typing import List

storage_nodes: List[tuple] = []

def storage_update():
    while True:
        for storage_node in storage_nodes:
            _socket = socket.socket() # Initiate connection to server

            try:
                _socket.connect((storage_node[0], storage_node[1]))
            except ConnectionRefusedError:
                print(f"{storage_node[0]}:{storage_node[1]} is down.")
                continue

            print(f"{storage_node[0]}:{storage_node[1]} is alive.")
            _socket.close()
            time.sleep(0.5)
        
        time.sleep(2)