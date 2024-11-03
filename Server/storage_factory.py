import socket
import time
from typing import List

storage_nodes: List[tuple] = []

def storage_update():
    while True:
        print("Checking storage nodes...")
        downed_nodes = []

        for storage_node in storage_nodes:
            _socket = socket.socket() # Initiate connection to server

            try:
                _socket.settimeout(5.0)
                _socket.connect((storage_node[0], storage_node[1]))
            except (ConnectionRefusedError, OSError):
                downed_nodes.append(storage_node)
                print(f"{storage_node[0]}:{storage_node[1]} is down.")
                continue

            print(f"{storage_node[0]}:{storage_node[1]} is alive.")
            _socket.close()
        
        # Remove all the downed nodes
        if len(downed_nodes) > 0:
            for downed_node in downed_nodes:
                storage_nodes.remove(downed_node)
                print(f"{downed_node[0]}:{downed_node[1]} has been removed from storage nodes.")
            
            # socket_server.py will handle the creation of new storage nodes
        
        time.sleep(2)