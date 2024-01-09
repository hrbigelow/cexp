"""
Leetcode Problem 1242
https://leetcode.com/problems/web-crawler-multithreaded/description/
"""

# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
#class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """

import asyncio
from functools import partial

class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        domain = startUrl.split('/')[2]
        visited = set()

        def is_valid_new(url):
            return url.split('/')[2] == domain and url not in visited

        async def step(url):
            visited.add(url)
            new_urls = await asyncio.to_thread(htmlParser.getUrls, url)
            valid_urls = filter(is_valid_new, new_urls)
            await asyncio.gather(*(step(url) for url in valid_urls))

        asyncio.run(step(startUrl))
        return list(visited)

