import sys
import requests
from concurrent import futures
import random
import time

def compute_summary(content):
    lines = content.split('\n')
    size = len(content)
    return f'Summary: {len(lines):8d} lines, {size:8d} bytes'

def output_content(url, summary):
    print(f'{summary}, {url}', flush=True)

def download_and_process(session, url):
    try:
        # time.sleep(0.05)
        response = session.get(url) # blocking
        content = response.content.decode()
        summary = compute_summary(content)
        output_content(url, summary)
    except BaseException as ex:
        print(f'Parsing {url}: Exception {ex}')


def main(url_list, num_tasks, max_threads):
    with open(url_list, 'r') as fh:
        urls = [ url.rstrip() for url in fh.readlines() ]

    start = time.perf_counter()
    tasks = random.choices(urls, k=num_tasks)
    session = requests.Session()
    with futures.ThreadPoolExecutor(max_workers=max_threads) as pool:
        for url in tasks:
            pool.submit(download_and_process, session, url)
    stop = time.perf_counter()
    print(f'Processing took {stop-start:.2f} seconds')


if __name__ == '__main__':
    url_list = sys.argv[1]
    num_tasks = int(sys.argv[2])
    num_threads = int(sys.argv[3])
    main(url_list, num_tasks, num_threads)


