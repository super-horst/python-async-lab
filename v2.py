import http.client
import concurrent.futures

REQUESTS=50000
POOL=10

def generate_work():
    num=0
    while num < REQUESTS:
        yield num
        num+=1

def drain_work_generator(work):
    try:
        connection = http.client.HTTPConnection('localhost:8080')
        while (item:=next(work)) is not None:
            #print(item)
            connection.request("GET", "/some.file")
            response = connection.getresponse().read()
    except StopIteration:
        pass
    finally:
        connection.close()

def gather_work_threads(executor, work):
    [executor.submit(drain_work_generator, work) for _p in range(POOL)]

if __name__ == "__main__":
    work = generate_work()
    with concurrent.futures.ThreadPoolExecutor(max_workers=POOL) as executor:
        gather_work_threads(executor, work)