import pickle
import socket
import threading
import time
from typing import List
from const import client_host, receive_port

storage_results = {}

def prepare_storage_server(data: List[str]):
    global storage_results

    if len(data) == 3:
        print(f"Connecting to leader storage server to duplicate storage ,..")
        storage_ip = data[1]
        storage_port = int(data[2])
        leader_storage_socket = socket.socket()
        leader_storage_socket.connect((storage_ip, storage_port))
        leader_storage_socket.send(f"get_all".encode())

        print("Connected to leader storage server. Awaiting storage data ...")

        while True:
            response_data = leader_storage_socket.recv(4096)
            storage_results = pickle.loads(response_data)
            print(storage_results)
            print("Received storage data from leader storage server. Data duplicated locally. Ready to serve.")
            break

def storage_loop():
    storage_socket = socket.socket()
    storage_socket.bind((client_host, receive_port))
    storage_socket.listen(10)
    print(f"Storage server listening on {client_host}:{receive_port}")

    while True:
        # Wait for new connections
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
    elif action == "get_all":
        storage_get_all(conn, address, parameters)
    elif action == "ping":
        pass

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
    print(f"Deleted {username} -> {llm_name} results.")
    del storage_results[username][llm_name]

def storage_get_all(conn, address, parameters):
    conn.send(pickle.dumps(storage_results))