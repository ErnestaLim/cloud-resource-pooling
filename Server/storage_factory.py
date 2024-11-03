import socket
import time
from typing import List
from const import slave_nodes

storage_nodes: List[tuple] = []

def storage_update():
    while True:
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

            #print(f"{storage_node[0]}:{storage_node[1]} is alive.")
            _socket.close()
        
        # Remove all the downed nodes
        if len(downed_nodes) > 0:
            for downed_node in downed_nodes:
                storage_nodes.remove(downed_node)
                print(f"{downed_node[0]}:{downed_node[1]} has been removed from storage nodes.")

                if len(slave_nodes) > 0:
                    slave_nodes.pop() # remove it, so that slave_process will disconnect the slave
            
            # if there is not enough slave nodes, it's okay, we'll wait until new nodes join the network
            # socket_server.py will handle the creation of new storage nodes
        
        time.sleep(2)