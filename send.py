import asyncio
from distributed import rpc

async def evaluate_llm():
    remote = rpc('192.168.1.7:8786')
    response = await remote.evaluate_llm()  
    remote.close_comms()
    print(response)

asyncio.run(evaluate_llm())