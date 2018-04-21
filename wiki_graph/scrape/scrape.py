from datetime import datetime, timedelta
import os
import random
import sys
import time
from typing import Set, Iterable, Optional, ClassVar
from urllib.parse import urlsplit, unquote

import attr
from bs4 import BeautifulSoup
import requests
import requests_html

# Epsilon value
EPS = sys.float_info.epsilon


@attr.s(slots=True, auto_attribs=True)
class WikiPageLinks(object):
    session: ClassVar[requests_html.HTMLSession] = requests_html.HTMLSession()
    base_url: ClassVar[str] = 'https://en.wikipedia.org'
    link_prefix: ClassVar[str] = 'wiki'
    req_timeout: ClassVar[timedelta] = timedelta(days=1)

    page_name: str = attr.ib(
        converter=lambda s: s.replace(' ', '_').lower())
    url: str = attr.ib(default=None)
    _html: Optional[requests_html.HTML] = attr.ib(default=None)
    _last_req: datetime = attr.ib(default=datetime.min)

    def __attrs_post_init__(self):
        self.url = '/'.join([self.base_url, self.link_prefix, self.page_name])

    @classmethod
    def from_url(cls, url: str):
        """Create a `WikiPageLinks` object from a url"""
        # Extract a page title from the url (just the last element of the path)
        page_name = os.path.split(urlsplit(url).path)[1]
        return cls(page_name)

    @classmethod
    def req(cls, url: str):
        """Make a request, sleeping for a random period of time afterwards"""
        res = cls.session.get(url)
        slp_tm = (random.random() + EPS) * 2.5  # Generate sleep time
        time.sleep(slp_tm)
        return res

    @property
    def html(self) -> requests_html.HTML:
        diff = datetime.utcnow() - self._last_req
        if self._html is None or diff > self.req_timeout:
            res = self.req(self.url)
            res.raise_for_status()
            self._html = res.html
            self._last_req = datetime.utcnow()
        return self._html

    @property
    def links(self) -> Set[str]:
        """Return relative paths (to normal wikipedia pages), except for the
        base page
        """
        pref = '/{p}/'.format(p=self.link_prefix)

        def _filt(x: str) -> bool:
            if 'Main_Page' in x:
                return False
            return x.startswith(pref) and (':' not in x)

        # Unescape quotes and filter out non-wiki pages
        def _map(x: str) -> str:
            return unquote(x.lower())
        uq_links = filter(_filt, map(_map, self.html.links))
        return set(uq_links).difference([pref + self.page_name])

    @property
    def absolute_links(self) -> Set[str]:
        return set(map(lambda x: self.base_url + x, self.links))


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
    pass
