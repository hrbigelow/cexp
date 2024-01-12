"""
1. create workers

When 

Unit of work:

1. get the url from queue
2. add to crawled set
3. call crawl
4. add the results to seen
5. 





"""
import sys
import asyncio


async def worker():
    nonlocal max_crawl, num_crawl, q
    while True:
        try:
            url = await q.get()
            next_urls = await crawl(url)
            crawled.add(url)
        except Exception as ex:
            print(f'Got exception {ex} crawling url {url}')
        finally:
            q.task_done()

        seen.add(next_urls)
        for next_url in next_urls:
            if num_crawl == max_crawl:
                break
            await q.put(next_url)
            num_crawl += 1

async def main(max_crawl, num_workers, start_url):
    q = asyncio.Queue()
    seen = set()
    crawled = set()
    await q.put(start_url)

    async with asyncio.TaskGroup() as tg:
        w = [ worker() for _ in range(num_workers) ]
    await q.join()
    print(f'Crawled {len(crawled)} URLs')
    print(f'Found {len(seen)} URLs')


if __name__ == '__main__':
    max_crawl = int(sys.argv[1])
    num_workers = int(sys.argv[2])
    start_url = sys.argv[3]
    asyncio.run(main(max_crawl, num_workers, start_url))


