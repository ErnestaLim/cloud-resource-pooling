import json
import socket
import time
import asyncio
from dask.distributed import Scheduler, Worker, Client
from distributed import SchedulerPlugin

def master_client_program():
    # host = '192.168.1.100'  # Server IP
    # port = 5000  # Server port
    host = socket.gethostbyname(socket.gethostname()) # Initiate connection to server
    port = 5000  # Server port number    
    client_socket = socket.socket() # Initiate connection to server
    client_socket.connect((host, port))    

    # Send initial identifer
    identification_data = "master"
    client_socket.send(identification_data.encode())

    # Flag
    broker_started: bool = False

    # Maintain connection till Server resolves client distribution
    while True:
        if not broker_started:
            # Simulate waiting for other script to call
            time.sleep(1)
            client_socket.send("request;1".encode())
            print("Requesting central server for 1 slave ...")

            # Wait for response (blocking call)
            response = client_socket.recv(1024).decode()
            response_data = json.loads(response)

            if response_data['success'] == False :
                print(f"Error: {response_data['message']}")
                print("Request failed. Retrying ...")
            else:
                broker_started = True
                print(f"Centeral server provided {len(response_data['addresses'])} nodes. Waiting for slave to connect ...")
                asyncio.get_event_loop().run_until_complete(master_loop())
        else:
            print("test")

    client_socket.close()  # close the connection

class MasterSchedulerPlugin(SchedulerPlugin):
    def __init__(self):
        super().__init__()

    def update_graph(self, scheduler, dsk=None, keys=None, restrictions=None, **kwargs):
        # Add custom processing logic here
        print("A task has been received by the scheduler.")
        # You can manipulate the graph or perform logging, pre-processing, etc.

async def master_loop():
    async with Scheduler(host=socket.gethostbyname(socket.gethostname()), port=8786) as scheduler:
        plugin = MasterSchedulerPlugin()
        scheduler.add_plugin(plugin)  # Register the custom plugin
        await scheduler.finished()    # Wait until the scheduler closes

if __name__ == '__main__':
    asyncio.run(master_loop())