import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin

def get_links(url:str) -> List[str]:
    """Get all the links on a page."""
    page = requests.get(url)
    bs = BeautifulSoup(page.content, features='lxml')
    links = [link.get("href") for link in bs.findAll('a')]
    absolute_urls = [urljoin(url, link) for link in links]
    return absolute_urls

def get_valid_links(valid_domain, url: str) -> List[str]:
    links = get_links(url)
    links = set(url.split('#')[0] for url in links)
    links = filter(lambda url: url.startswith(valid_domain), links)
    return links

