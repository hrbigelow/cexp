import sys
import asyncio
import functools

from ..crawl_base import get_valid_links

visited = set()
tasks = []

async def next_links(domain, url):
    links = await asyncio.to_thread(get_valid_links, domain, url)
    return links

async def trampoline(coro_fn, init_val):
    await asyncio.sleep(0.1)
    vals = await coro_fn(init_val)
    for val in vals:
        if val in visited:
            continue
        task = asyncio.create_task(trampoline(coro_fn, val))
        visited.add(val)
        tasks.append(task)

async def main(domain):
    coro_fn = functools.partial(next_links, domain)
    task = asyncio.create_task(trampoline(coro_fn, domain))
    tasks.append(task)
    while not all(t.done() for t in tasks):
        print(f'{len(tasks)}')
        await asyncio.gather(*tasks) 

# The approach I had suggested initially
# All tasks are added to `tg` context manager
async def trampoline_tg(coro_fn, init_val, tg):
    vals = await coro_fn(init_val)
    for val in vals:
        if val in visited:
            continue
        tg.create_task(trampoline_tg(coro_fn, val, tg))
        visited.add(val)

async def main_tg(domain):
    coro_fn = functools.partial(next_links, domain)
    async with asyncio.TaskGroup() as tg:
        # any tasks added to tg must complete before __aexit__ returns
        tg.create_task(trampoline_tg(coro_fn, domain, tg))

if __name__ == '__main__':
    mode = sys.argv[1]
    domain = sys.argv[2]
    if mode == 'wait': 
        asyncio.run(main(domain))
    else:
        asyncio.run(main_tg(domain))

print(f'Found {len(visited)} links')
print('\n'.join(visited))

# print(get_links(website_to_crawl))

def all_links(domain):

    visited = set()

    def crawl(start_url):
        # print(f'crawling {start_url}')
        urls = get_links(start_url)

        for anchor in urls:
            url = anchor.split('#')[0]
            if url in visited:
                continue
            if not url.startswith(domain):
                continue
            visited.add(url)
            crawl(url)
    start_url = domain

    crawl(start_url)

    return sorted(visited)

# links = all_links(website_to_crawl)
# print(f'Found {len(links)}')





