from dask.distributed import Client

def compute_task():
    return 10

client = Client('192.168.1.7:8786')
future = client.submit(compute_task)
result = future.result()

print("Result:", result)