import sys
import asyncio
import httpx
import random
import time

def compute_summary(content):
    # lines = content.split('\n')
    num_lines = content.count('\n') + 1
    size = len(content)
    return f'Summary: {num_lines:8d} lines, {size:8d} bytes'

def output_content(url, summary):
    print(f'{summary}, {url}', flush=True)

async def download_and_process_async(client, url):
    global global_sem
    try:
        async with global_sem:
            # await asyncio.sleep(0.1)
            response = await client.get(url) # third-party non-blocking variant of HTTP get
        content = response.text
        summary = compute_summary(content)
        output_content(url, summary)
    except BaseException as ex:
        print(f'Got exception for {url}: {ex}')

global_sem = asyncio.Semaphore(200)

async def main_async(url_list, num_tasks):
    with open(url_list, 'r') as fh:
        urls = [ url.rstrip() for url in fh.readlines() ]

    tasks = random.choices(urls, k=num_tasks)
    start = time.perf_counter()

    limits = httpx.Limits(max_connections=500)
    timeout = httpx.Timeout(None)


    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client, \
            asyncio.TaskGroup() as tg:
        print('Starting task creation', file=sys.stderr, flush=True)
        for i, url in enumerate(tasks):
            tg.create_task(download_and_process_async(client, url))
            if i % 10 == 0:
                await asyncio.sleep(0)
        print('Finished task creation', file=sys.stderr, flush=True)
            # futs.append(fut)
        # await asyncio.wait(futs, return_when=asyncio.FIRST_EXCEPTION)
        # await asyncio.wait(futs)

    stop = time.perf_counter()
    print(f'Total {stop-start:.2f} seconds')

if __name__ == '__main__':
    url_list = sys.argv[1]
    num_tasks = int(sys.argv[2])
    asyncio.run(main_async(url_list, num_tasks))

