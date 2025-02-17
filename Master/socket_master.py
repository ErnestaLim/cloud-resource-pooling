import argparse
import glob
import json
import os
import pickle
import socket
import subprocess
import threading
import time
import asyncio
from typing import List
from llm_tasks import LLMTask

# Set up argument parser
parser = argparse.ArgumentParser(description='Client program to connect to a server.')
parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
parser.add_argument('--port', type=int, default=5000, help='Server port number')
args = parser.parse_args()

host = args.ip # Initiate connection to server
port = args.port  # Server port number    

# Store tasks locally in json
TASK_FILE = "test.json"

def save_tasks_to_file(tasks: List[LLMTask]):
    try:
        # Convert tasks to a list of dictionaries
        tasks_data = [task.to_dict() for task in tasks]
        with open(TASK_FILE, 'w') as f:
            json.dump(tasks_data, f)
        #print("Data saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def load_tasks_from_file() -> List[LLMTask]:
    try:
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, 'r') as f:
                tasks_data = json.load(f)
            print("Tasks loaded from file.")
            return [LLMTask.from_dict(task) for task in tasks_data]
        return []
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return []

def request_slaves(amount: int):
    client_socket = socket.socket()  # Initiate connection to server
    connected = False  # Flag to track connection status

    while not connected:
        try:
            client_socket.connect((host, port))
            connected = True
        except ConnectionRefusedError:
            print("Failed to connect to server. Retrying ...")
            time.sleep(2)

    # Send initial identifier
    identification_data = "master"
    client_socket.send(identification_data.encode())

    # Maintain connection till server resolves client distribution
    while True:
        time.sleep(2)

        client_socket.send(f"request;{amount}".encode())
        print(f"Requesting central server for {amount} slave(s) ...")

        # Wait for response (blocking call)
        response = client_socket.recv(1024).decode()
        response_data = json.loads(response)

        if response_data['success'] == False:
            print(f"Error: {response_data['message']}")
            print("Request failed. Retrying ...")
        else:
            client_socket.close()
            break

    return response_data['addresses']

def get_storage_nodes():
    client_socket = socket.socket()  # Initiate connection to server
    connected = False  # Flag to track connection status

    # Attempt to connect until successful
    while not connected:
        try:
            client_socket.connect((host, port))
            connected = True
        except ConnectionRefusedError:
            print("Failed to connect to server. Retrying ...")
            time.sleep(2)  # Wait before retrying

    # Send initial identifier
    message = "get_storage_nodes"
    client_socket.send(message.encode())

    # Wait for response (blocking call)
    response = client_socket.recv(4096)
    storage_nodes = pickle.loads(response)

    client_socket.close()  # Ensure socket is closed after receiving the response
    return storage_nodes

slave_nodes: List[socket.socket] = []
llm_tasks: List[LLMTask] = load_tasks_from_file() # Initialize llm_tasks by loading from file else []

def handle_conn(conn: socket.socket, address: tuple):
    parameters = conn.recv(1024).decode().split(";")
    action = parameters[0]
    
    if action == "do_llm_eval":
        task_process(conn, address, parameters)
    elif action == "connect":
        slave_process(conn, address)

def task_process(conn: socket.socket, address: tuple, parameters: List[str]):
    global llm_tasks
    
    username = parameters[1]
    llm_name = parameters[2]

    if not any(task.username == username and task.llm_name == llm_name for task in llm_tasks):
        print(f"Received task from {username} -> {llm_name}.")
        llm_tasks.append(LLMTask(username, llm_name))
        save_tasks_to_file(llm_tasks)
        request_slaves(4)
    else:
        print(f"Task from {username} -> {llm_name} already exists. Skipping ...")

    results = {
        "tinyMMLU": None,
        "tinyHellaswag": None,
    }

    # Wait for the task to complete, by checking with storage nodes
    while any(value is None for value in results.values()):
        time.sleep(2)
        #print("Waiting for storage nodes to send results ...")
        storage_nodes = get_storage_nodes()
        
        for storage_node in storage_nodes:
            storage_socket = socket.socket() # Initiate connection to server
            storage_socket.connect((storage_node[0], storage_node[1]))    

            # Send retrieve action
            message = f"retrieve;{username};{llm_name}"
            storage_socket.send(message.encode())

            # Receive response data from the server
            response_data = storage_socket.recv(4096)
            result = pickle.loads(response_data)
            
            # Check if result is not None and set it in the dictionary
            if result is not None:
                for key, value in result.items():
                    if key in results and results[key] is None:
                        results[key] = value
            
            storage_socket.close()
    
    print("All results received. Deleting results from storage nodes ...")

    # Delete from storage nodes
    storage_nodes = get_storage_nodes()
    for storage_node in storage_nodes:
        storage_socket = socket.socket() # Initiate connection to server
        storage_socket.connect((storage_node[0], storage_node[1]))    

        # Send delete action
        message = f"delete;{username};{llm_name}"
        storage_socket.send(message.encode())

        # Delete from our own storage too
        llm_tasks = [task for task in llm_tasks if not (task.username == username and task.llm_name == llm_name)]

        storage_socket.close()
    
    print("Deleted results from storage nodes. Replying to user request ...")
    
    # Send results back to user
    conn.sendall(pickle.dumps(results))

def slave_process(conn: socket.socket, address: tuple):
    print(f"Slave {address[0]}:{address[1]} connected.")
    slave_nodes.append(conn)
    
    # Get the first LLMTask that is not assigned
    current_job: LLMTask = next((task for task in llm_tasks if not task.assigned), None)
    
    # If there is no task, we don't need to slave. So we disconnect it by returning this function.
    if current_job is None:
        return

    while current_job.accessed:
        pass

    # Consumer, Producer thread blocking
    current_job.accessed = True

    # If there is a task, we assign it to the slave. First, we determine which task it is.
    if current_job.tinyMMLU < 2:
        #print("send mmlu")
        #print(current_job.tinyMMLU)
        conn.send(f"do_llm_eval;{current_job.username};{current_job.llm_name};tinyMMLU".encode())
        current_job.tinyMMLU += 1
    elif current_job.tinyHellaswag < 2:
        #print("send hellaswag")
        #print(current_job.tinyHellaswag)
        conn.send(f"do_llm_eval;{current_job.username};{current_job.llm_name};tinyHellaswag".encode())
        current_job.tinyHellaswag += 1
    
    # After you finish the above if statement, the task is now 2. So if this is the last beanchmark and it's two, we pop it from our task list
    if current_job.tinyHellaswag >= 2:
        current_job.assigned = True
    
    current_job.accessed = False
    save_tasks_to_file(llm_tasks)

async def master_loop():
    host = socket.gethostbyname(socket.gethostname()) # Get the server hostname or IP
    port = 8786 # Define server port    
    server_socket = socket.socket() # Create socket instance
    server_socket.bind((host, port)) # Bind the server to the host and port

    server_socket.listen(10) # Listen for up to X clients simultaneously
    print(f"Master listening on {host}:{port}")

    while True:
        conn, address = server_socket.accept() # Accept new connections
        client_thread = threading.Thread(target=handle_conn, args=(conn, address)) # Create a new thread for each client
        client_thread.start()

if __name__ == '__main__':
    asyncio.run(master_loop())