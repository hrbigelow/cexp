import fire
import asyncio
import httpx

"""
Testing the concurrent download of a list of URLs
"""

def main(url_list, max_concur_req):
    with open(url_list, 'r') as fh:
        urls = [url.rstrip() for url in fh.readlines()]
    max_concur_sem = asyncio.Semaphore(max_concur_req)

    async def download(url):
        async with max_concur_sem:
            resp = await httpx.get(url)
            results[url] = resp.text

    results = {}

    try:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                task = tg.create_task(download(url))
                results.add(task)
    except* Exception as eg:
        eg.
        for subex in eg.exceptions:
            pass
    else:
        for res in results:





if __name__ == '__main__':
    fire.Fire(main)
