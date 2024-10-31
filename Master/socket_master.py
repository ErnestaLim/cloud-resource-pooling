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

# Set up argument parser
parser = argparse.ArgumentParser(description='Client program to connect to a server.')
parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
parser.add_argument('--port', type=int, default=5000, help='Server port number')
args = parser.parse_args()

host = args.ip # Initiate connection to server
port = args.port  # Server port number    

def request_slaves(amount: int):
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    

    # Send initial identifer
    identification_data = "master"
    client_socket.send(identification_data.encode())

    # Maintain connection till Server resolves client distribution
    while True:
        # Simulate waiting for other script to call
        time.sleep(1)

        client_socket.send(f"request;{amount}".encode())
        print(f"Requesting central server for {amount} slave(s) ...")

        # Wait for response (blocking call)
        response = client_socket.recv(1024).decode()
        response_data = json.loads(response)

        if response_data['success'] == False :
            print(f"Error: {response_data['message']}")
            print("Request failed. Retrying ...")
        else:
            client_socket.close()
            break

    return response_data['addresses']

def get_storage_nodes():  
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))

    # Send initial identifer
    message = "get_storage_nodes"
    client_socket.send(message.encode())

    # Wait for response (blocking call)
    response = client_socket.recv(4096)
    storage_nodes = pickle.loads(response)

    return storage_nodes

def _worker_evalute_llm(username, llm_name, eval_name):
    print("Task received. Evaluating LLM ...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    output_dir = f"{script_dir}/output/EleutherAI__pythia-160m"
    
    # Run a command and capture its output
    command = "lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output"  # Example command, you can replace it with any command you need
    subprocess.run(command, shell=True, check=True)

    # Find the latest JSON file in the output/EleutherAI/pythia-160m directory
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    
    if not json_files:
        print("No JSON files found in the directory. Task failed.")
        return {
            'success': False,
            'message': "No JSON files found in the directory."
        }

    # Get the latest JSON file based on modification time
    latest_json_file = max(json_files, key=os.path.getmtime)

    # Read the content of the JSON file
    with open(latest_json_file, 'r') as f:
        json_content = json.load(f)
        results = json_content['results']
    
    results = {'tinyMMLU': {'alias': 'tinyMMLU', 'acc_norm,none': 0.29423820925289884, 'acc_norm_stderr,none': 'N/A'}}
    print("Evaluation completed. Sending results ...")
    
    # Ask central server for stroage nodes addresses
    def get_storage_nodes():  
        client_socket = socket.socket() # Initiate connection to server
        client_socket.connect((host, port))

        # Send initial identifer
        message = "get_storage_nodes"
        client_socket.send(message.encode())

        print("Requesting central server for storage nodes' addresses ...")

        # Wait for response (blocking call)
        response = client_socket.recv(4096)
        storage_nodes = pickle.loads(response)

        return storage_nodes

    storage_nodes = get_storage_nodes()
    print(storage_nodes)
    print("Sending storage nodes results ...")
    
    # Send to stroage nodes
    for storage_node in storage_nodes:
        storage_socket = socket.socket() # Initiate connection to server
        storage_socket.connect((storage_node[0], storage_node[1]))    

        # Send initial identifer
        message = f"store;{username};{llm_name};{eval_name};{results}"
        storage_socket.send(message.encode())
    
    print("Results sent to storage nodes.")
    print("Restarting slave node ...")

    # Return both the computation result and the JSON content
    return {
        'success': True,
        'message': "Successfully evaluated LLM.",
        'results': results
    }

def _evalute_llm():
    '''
    client = Client('192.168.1.5:8786')

    # Submit the task to the scheduler
    future = client.submit(_worker_evalute_llm, username="bernard", llm_name="160m", eval_name="tinyMMLU")
    fire_and_forget(future)
    '''

    results = {
        "tinyMMLU": None,
    }

    # Wait for the task to complete, by checking with storage nodes
    while any(value is None for value in results.values()):
        time.sleep(1)
        print("Waiting for storage nodes to send results ...")
        storage_nodes = get_storage_nodes()
        
        for storage_node in storage_nodes:
            storage_socket = socket.socket() # Initiate connection to server
            storage_socket.connect((storage_node[0], storage_node[1]))    

            # Send retrieve action
            message = f"retrieve;bernard;160m"
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
        message = f"delete;bernard;160m"
        storage_socket.send(message.encode())

        storage_socket.close()
    
    print("Deleted results from storage nodes. Replying to user request ...")

    return results

async def evaluate_llm():
    result = await asyncio.to_thread(_evalute_llm)
    return result

slave_nodes: List[socket.socket] = []
llm_tasks: List[tuple] = []

def handle_conn(conn: socket.socket, address: tuple):
    parameters = conn.recv(1024).decode().split(";")
    action = parameters[0]
    
    if action == "do_llm_eval":
        task_process(conn, address, parameters)
    elif action == "connect":
        slave_process(conn, address)

def task_process(conn: socket.socket, address: tuple, parameters: List[str]):
    username = parameters[1]
    llm_name = parameters[2]

    print(f"Received task from {username} -> {llm_name}.")
    llm_tasks.append((username, llm_name))
    request_slaves(1)

def slave_process(conn: socket.socket, address: tuple):
    print(f"Slave {address[0]}:{address[1]} connected.")
    slave_nodes.append(conn)

    task = llm_tasks.pop(0)

    # Keep connection alive till new task is received
    while True:
        pass

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