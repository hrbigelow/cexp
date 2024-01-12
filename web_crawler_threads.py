from crawl_base import get_valid_links

import time
import sys
from typing import List
import functools

from concurrent import futures

# class WaitingThreadPoolExecutor(futures.ThreadPoolExecutor):
    # def shutdown(self, wait=True, *, cancel_futures=False):


def crawl(pool, url) -> None:
    visited.add(url)
    new_urls = links_fn(url)
    new_urls = list(filter(lambda url: url not in visited, new_urls))
    if len(new_urls) == 0:
        return
    print(f'Found {len(new_urls)} urls inside crawl')
    futs = pool.map(functools.partial(crawl, pool), new_urls)
    futures.wait(list(futs))

visited = set()
start_url = 'https://andyljones.com'
links_fn = functools.partial(get_valid_links, start_url)
    
def main(start_url):
    # visited = set()
    # I thought that the context manager __exit__ method waits for all
    # pending futures to finish
    with futures.ThreadPoolExecutor() as pool:
        fut = pool.submit(crawl, pool, start_url)
        futures.wait([fut])
    print(f'Found {len(visited)} links')

if __name__ == '__main__':
    start_url = sys.argv[1]
    main(start_url)





