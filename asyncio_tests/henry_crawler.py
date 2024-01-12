"""
Based on Murphy's crawler, but not using a worker function or queues.
Instead, recursively calls create_task for each new URL
"""
import sys
import time
import asyncio
import httpx
from crawl import UrlFilterer, UrlParser
from typing import Callable, Iterable

"""
Is there some abstract function that can be a 'trampoline' but for tasks?

It should:

1. accept a coroutine with signature A -> set[A] 
2. creates a task to run the coroutine
3. collects the output, and schedules more of them

"""

class Spider:
    """
    Class for running a coroutine of Callable[str, set[str]]
    recursively on its own results.
    Allow at most max_workers to suspend inside the coro at a time
    Allow at most max_calls of the coro

    Call as:

    spider = Spider(max_workers, max_calls)
    try:
        async with asyncio.TaskGroup() as tg:
            await spider.run(coro_fn, start_vals, tg)
    except BaseException as ex:
        ...
    """
    def __init__(
            self,
            max_workers: int, 
            max_calls: int,
            ):
        # Schedule max_
        self.max_workers = asyncio.Semaphore(max_workers)
        self.calls_left = max_calls
        
    async def run(
            self,
            coro_fn: Callable[str, set[str]], 
            vals: set[str], 
            tg: asyncio.TaskGroup,
            ):
        # Run the coro_fn on the initial set of vals
        # Run every call of the coro as a task inside tg.
        await self._run(True, coro_fn, vals, tg)

    async def _run(
            self,
            first_call: bool,
            coro_fn: Callable[str, set[str]], 
            val: str | set[str], 
            tg: asyncio.TaskGroup,
            ):
        if self.calls_left == 0:
            return
        self.calls_left -= 1

        if first_call:
            vals = val
        else:
            async with self.max_workers:
                vals = await coro_fn(val)
        for val in vals:
            coro = self._run(False, coro_fn, val, tg)
            tg.create_task(coro)

class Crawler:
    def __init__(
            self,
            client: httpx.AsyncClient,
            urls: Iterable[str],
            filter_url: Callable[[str, str], str | None],
            workers: int = 10,
            limit: int = 25,
            ):
        self.client = client
        self.start_urls = set(urls)
        self.seen = set()
        self.filter_url = filter_url
        self.max_workers = workers
        self.limit_crawl = limit
        self.total_crawled = 0

    def parse_links(self, base: str, text: str) -> set[str]:
        parser = UrlParser(base, self.filter_url)
        parser.feed(text)
        return parser.found_links

    async def crawl(self, url: str):
        print(f'Crawling {url}')
        await asyncio.sleep(0.1)
        response = await self.client.get(url, follow_redirects=True)

        found_links = self.parse_links(
            base=str(response.url),
            text=response.text,
        )
        self.seen.update(found_links)
        return found_links

    async def run(self):
        self.seen.update(self.start_urls)
        spider = Spider(self.max_workers, self.limit_crawl)
        try:
            async with asyncio.TaskGroup() as tg:
                await spider.run(self.crawl, self.start_urls, tg)
        except BaseException as ex:
            print(f'Exception: {ex.message}')
            for subex in ex.exceptions:
                print(subex)
        return

async def main(domain, workers, limit):
    filterer = UrlFilterer(
        allowed_domains={domain},
        allowed_schemes={"http", "https"},
        allowed_filetypes={".html", ".php", ""},
    )

    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        crawler = Crawler(
            client=client,
            urls=['https://' + domain],
            filter_url=filterer.filter_url,
            workers=workers,
            limit=limit,
        )
        await crawler.run()
    end = time.perf_counter()

    seen = sorted(crawler.seen)
    # print("Results:")
    # for url in seen:
        # print(url)
    print(f"Crawled: {crawler.total_crawled} URLs")
    print(f"Found: {len(seen)} URLs")
    print(f"Done in {end - start:.2f}s")


if __name__ == '__main__':
    domain = sys.argv[1]
    workers = int(sys.argv[2])
    limit = int(sys.argv[3])
    asyncio.run(main(domain, workers, limit), debug=False)
    # asyncio.get_event_loop().run_until_complete(main())

