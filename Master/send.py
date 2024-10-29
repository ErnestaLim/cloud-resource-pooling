import asyncio
from distributed import rpc

async def send_add():
    remote = rpc('192.168.1.7:8786')
    response = await remote.add(x=10, y=20)  
    remote.close_comms()  
    print(response)

asyncio.run(send_add())