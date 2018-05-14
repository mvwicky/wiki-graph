import abc
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


class AbstractNode(abc.ABC):
    @property
    @abc.abstractmethod
    def url(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def page_name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def links(self) -> Set[str]:
        ...


@attr.s(slots=True, auto_attribs=True)
class WikiPage(AbstractNode):
    """A single node in the graph: a wikipedia page
    Class Variables:
    session: a requests_html session, for getting the actual page markup,
             which is parsed
    base: the base wikipedia address, hypothetically could be changed to point
          to non-english wikis
    prefix: the part that goes between base and the page name
    req_timeout: age of a request after which time we consider it stale

    Instance Variables:
    _page_name: the name of the page which this node represents
    _url: the url of the page which this node represents
    _html: the markup of the page
    _links: a set containing the links contained on this page
    _last_req: the date/time of the last request, so we can periodically
               refresh the page
    """
    session: ClassVar[requests_html.HTMLSession] = requests_html.HTMLSession()
    base: ClassVar[str] = 'https://en.wikipedia.org'
    prefix: ClassVar[str] = 'wiki'
    req_timeout: ClassVar[timedelta] = timedelta(days=1)

    _page_name: str = attr.ib(
        converter=lambda s: str(s).replace(' ', '_'))
    _url: str = attr.ib(default=attr.Factory(
        lambda s: '/'.join([s.base, s.prefix, s._page_name]), takes_self=True))
    _html: Optional[requests_html.HTML] = attr.ib(init=False, default=None)
    _links: Set[str] = attr.ib(
        init=False, repr=False, default=attr.Factory(set))
    _last_req: datetime = attr.ib(init=False, default=datetime.min)

    @classmethod
    def from_url(cls, url: str):
        """Create a `WikiPageLinks` object from a url"""
        # Extract a page title from the url (just the last element of the path)
        page_name = os.path.split(urlsplit(url).path)[1]
        return cls(page_name)

    @classmethod
    def req(cls, url: str) -> requests.Request:
        """Make a request, sleeping for a random period of time afterwards"""
        res = cls.session.get(url)
        slp_tm = (random.random() + EPS) * 2.5  # Generate sleep time
        time.sleep(slp_tm)
        return res

    @property
    def page_name(self) -> str:
        return self._page_name

    @property
    def url(self) -> str:
        return self._url

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
    def title(self) -> str:
        return self.html.find('title', first=True).text

    @property
    def links(self) -> Set[str]:
        """Return relative paths (to normal wikipedia pages), except for the
        base page
        """
        diff = datetime.utcnow() - self._last_req
        if not self._links or diff > self.req_timeout:
            pref = '/{p}/'.format(p=self.prefix)

            def _filt(x: str) -> bool:
                if 'Main_Page' in x:
                    return False
                return x.startswith(pref) and (':' not in x)

            def _map(x: str) -> str:
                return unquote(x)
            # Unescape quotes and filter out non-wiki pages
            uq_links = filter(_filt, map(_map, self.html.links))
            self._links = set(uq_links).difference([pref + self.page_name])
        return self._links

    @property
    def absolute_links(self) -> Set[str]:
        return set(map(lambda x: self.base + x, self.links))


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
