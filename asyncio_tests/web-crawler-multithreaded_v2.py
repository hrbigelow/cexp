
import asyncio
from functools import partial

class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        domain = startUrl.split('/')[2]
        visited = set()

        def is_valid_new(url):
            return url.split('/')[2] == domain and url not in visited

