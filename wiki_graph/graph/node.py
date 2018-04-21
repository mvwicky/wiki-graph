import os
import random
import sys
import time
from typing import ClassVar, List
from urllib.parse import urlsplit

import attr
from bs4 import BeautifulSoup
import requests


@attr.s(slots=True)
class WikiNode(object):
    """A Graph Node
    TODO: Change outpaths to be a list of integers, indices to a global list
          Maybe just change everything to indices"""
    wiki_url: ClassVar[str] = 'https://en.wikipedia.org'
    link: str = attr.ib()
    level: int = attr.ib()
    out_paths: List[str] = attr.ib(default=attr.Factory(list))

    @property
    def page_name(self) -> str:
        return os.path.split(urlsplit(self.link).path)[1]

    @staticmethod
    def wiki_links(tag) -> bool:
        href = tag.attrs.get('href')
        if href is None:
            return False
        if 'Main_Page' in href:
            return False
        return href.startswith('/wiki') and (':' not in href)

    @classmethod
    def with_links(cls, url):
        ret = cls(url)
        ret.get_links()
        return ret

    def find_links(self):
        """Return a set of links from a page"""
        links = set()  # Use a set so we don't duplicate
        res = req(self.link)
        if res.status_code != requests.codes.ok:
            return links
        soup = BeautifulSoup(res.content, 'lxml')
        for link in soup(self.wiki_links):
            links.add(''.join((self.wiki_url, link['href'])))
        links -= {self.link}
        return links

    def get_links(self):
        self.out_paths.extend(self.find_links())
