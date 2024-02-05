import aiohttp
import asyncio

REQUESTS=50000
POOL=10

def generate_work():
    num=0
    while num < REQUESTS:
        yield num
        num+=1

async def drain_work_generator(work):
    try:
        async with aiohttp.ClientSession('http://localhost:8080') as session:
            while (item:=next(work)) is not None:
                #print(item)
                async with session.get("/some.file") as response:
                    _html = await response.text()
    except StopIteration:
        pass

async def gather_work_tasks(work):
    tasks=[asyncio.create_task(drain_work_generator(work)) for _p in range(POOL)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    work = generate_work()
    asyncio.run(gather_work_tasks(work))
