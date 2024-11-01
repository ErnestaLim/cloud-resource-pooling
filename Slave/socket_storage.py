import pickle
import socket
import threading
import time
from typing import List

client_host = "0.0.0.0"
receive_port = 51592

storage_results = {}

def storage_loop(client_socket: socket.socket):
    client_socket.send(f"start_storage_node;{receive_port}".encode())
    client_socket.settimeout(10)
    threading.Thread(target=storage_thread).start()

    while True:
        time.sleep(5)
        print("Heartbeat sent to server")
        try:
            client_socket.send("heartbeat".encode())
        except BrokenPipeError:
            print("Server has disconnected.")
            break

        data: List[str] = client_socket.recv(1024).decode().split(";")
        action = data[0]

        if action == 'heartbeat-ack':
            print("Heartbeat acknowledged by server.")

def storage_thread():
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