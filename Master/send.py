from dask.distributed import Client

def compute_task():
    return 10

client = Client('192.168.1.7:8786')
client._send_to_scheduler({'op': 'add', 'x': 1, 'y': 2})