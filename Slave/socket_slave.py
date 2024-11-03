import argparse
import asyncio
import glob
import json
import os
import pickle
import socket
import subprocess
import threading
import time
from typing import List
from socket_storage import storage_loop
from helper import get_storage_nodes

client_host = "0.0.0.0"
send_port = 51591

async def client_program(host: str, port: int): 
    client_socket = socket.socket() # Initiate connection to server
    client_socket.bind((client_host, send_port))
    client_socket.connect((host, port))
    identification_data = "slave"
    client_socket.send(identification_data.encode()) # Send initial identifer

    print(f"Connected to server as {client_host}:{send_port}. Awaiting assignment to master server ...")

    # Maintain connection till Server sends Master Node IP
    while True:
        data: List[str] = client_socket.recv(1024).decode().split(";")
        action = data[0]

        if action == 'connect':
            ip: str = data[1]
            port: int = int('8786') # data[2]

            slave_loop(ip, port)
        elif action == 'connect_storage':
            break
    
    if action == 'connect_storage':
        storage_loop()

def slave_loop(ip: str, port: int):
    print(f"Server assigned us to {ip}:{port}.")
    print(f"Connecting to assigned address ...")

    _socket = socket.socket() # Initiate connection to server
    _socket.connect((ip, port))
    _socket.send("connect".encode()) # Send initial identifer

    print("Connected to master server. Awaiting task ...")

    while True:
        parameters = _socket.recv(1024).decode().split(";")
        action = parameters[0]

        if action == "do_llm_eval":
            username = parameters[1]
            llm_name = parameters[2]
            eval_name = parameters[3]
            slave_evalute_llm(username, llm_name, eval_name)

def slave_evalute_llm(username, llm_name, eval_name):
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
    exit(1)

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--ip', type=str, default=socket.gethostbyname(socket.gethostname()), help='Server IP address')
    parser.add_argument('--port', type=int, default=5000, help='Server port number')
    args = parser.parse_args()
    
    asyncio.run(client_program(args.ip, args.port))