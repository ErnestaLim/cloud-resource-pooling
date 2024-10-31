import glob
import json
import os
import socket
import subprocess
import time
import asyncio
from dask.distributed import Scheduler, Worker, Client, fire_and_forget
from distributed import SchedulerPlugin

def request_slaves(amount: int):
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port
    host = socket.gethostbyname(socket.gethostname()) # Initiate connection to server
    port = 5000  # Server port number    
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
            print(f"Centeral server provided {len(response_data['addresses'])} nodes. Waiting for slave to connect ...")
            client_socket.close()
            break

    return response_data['addresses']

# Runs on storage node
def _storage_node_store(msater_address, result):
    # Store the result in the storage node
    pass

def _worker_evalute_llm(storage_nodes):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    output_dir = f"{script_dir}/output/EleutherAI__pythia-160m"
    
    # Run a command and capture its output
    command = "lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output"  # Example command, you can replace it with any command you need
    subprocess.run(command, shell=True, check=True)

    # Find the latest JSON file in the output/EleutherAI/pythia-160m directory
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    
    if not json_files:
        return {
            'success': False,
            'message': "No JSON files found in the directory."
        }

    # Get the latest JSON file based on modification time
    latest_json_file = max(json_files, key=os.path.getmtime)

    # Read the content of the JSON file
    with open(latest_json_file, 'r') as f:
        json_content = json.load(f)

    # Return both the computation result and the JSON content
    return {
        'success': True,
        'message': "Successfully evaluated LLM.",
        'json_content': json_content
    }

def _evalute_llm():
    client = Client('192.168.1.5:8786')

    # Get two dedicated volunteer nodes from the server
    print("Requesting 2 storage nodes from the server ...")
    storage_nodes = request_slaves(2)

    for storage_node in storage_nodes:
        pass
    
    # Get one node for LLM evaluation
    print("Requesting 1 node for LLM evaluation ...")
    llm_nodes = request_slaves(1)

    # Submit the task to the scheduler
    future = client.submit(_worker_evalute_llm, workers=f"{llm_nodes[0][0]}:{llm_nodes[0][1]}", storage_nodes=storage_nodes)
    fire_and_forget(future)

    return 22

async def evaluate_llm():
    result = await asyncio.to_thread(_evalute_llm)
    return result

class MasterSchedulerPlugin(SchedulerPlugin):
    def __init__(self):
        super().__init__()

    # On new custom task received
    def update_graph(self, scheduler, dsk=None, keys=None, restrictions=None, **kwargs):
        # TODO: If not LLM eval, request for one slave
        pass

async def master_loop():
    async with Scheduler(host=socket.gethostbyname(socket.gethostname()), port=8786) as scheduler:
        scheduler.handlers["evaluate_llm"] = evaluate_llm
        plugin = MasterSchedulerPlugin()
        scheduler.add_plugin(plugin)  # Register the custom plugin
        await scheduler.finished()    # Wait until the scheduler closes

if __name__ == '__main__':
    asyncio.run(master_loop())