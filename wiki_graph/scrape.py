import os
from typing import Set, Iterable
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup
import requests


def pct_decode(inp: str) -> str:
    return unquote(inp)


def wiki_links(tag) -> bool:
    href = tag.attrs.get('href')
    if href is None:
        return False

    if 'Main_Page' in href:
        return False

    return href.startswith('/wiki') and (':' not in href)


def name_to_url(page_name: str) -> str:
    wiki_en = 'https://en.wikipedia.org'
    return '/'.join((wiki_en, 'wiki', page_name))


def page_links(page_name: str) -> Set[str]:
    wiki_en = 'https://en.wikipedia.org'
    url = '/'.join((wiki_en, 'wiki', page_name))
    res = requests.get(url)
    links = set()
    if res.status_code != requests.codes.ok:
        return links

    soup = BeautifulSoup(res.content, 'lxml')
    for link in soup(wiki_links):
        links.add(''.join((wiki_en, link['href'])))
    links -= {url}
    return links


def links_to_names(links: Iterable[str]) -> Iterable[str]:
    return map(lambda x: os.path.split(urlsplit(x).path)[1], links)


if __name__ == '__main__':
    import requests_html

    url = 'https://en.wikipedia.org/wiki/George_Washington'
    ses = requests_html.Session()
    res = ses.get(url)
    for link in res.html.links:
        if link.startswith('/wiki'):
            print(pct_decode(link))
