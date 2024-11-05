import socket
from typing import List

slave_nodes: List[socket.socket] = []
master_nodes: List[socket.socket] = []
MINIMUM_STORAGE_NODES = 2