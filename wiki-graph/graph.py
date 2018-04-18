import os
from collections import deque
from typing import List, ClassVar, Union

import attr
import requests

from scrape import name_to_url
from node import WikiNode


@attr.s(slots=True)
class WikiGraph(object):
    """From a starting Wikipedia article (nodes[0]), view the pages to which it
    links, to a specified depth

    nodes: a list of pages, which store their link and the pages to which they
           link
    adj: an adjacency list (probably gonna be deleted)
    node_map: maps links to nodes indicies"""

    nodes: List[WikiNode] = attr.ib(default=attr.Factory(list))
    # Adjacency List
    adj: dict = attr.ib(default=attr.Factory(dict))
    # Map url to adjacency matrix index
    node_map: dict = attr.ib(default=attr.Factory(dict))

    def __contains__(self, item: Union[str, WikiNode]):
        if isinstance(item, str):
            return item in self.node_map
        elif isinstance(item, WikiNode):
            return item.link in self.node_map
        else:
            raise NotImplementedError

    def __iter__(self):
        return iter(self.nodes)

    @classmethod
    def new_dfs(cls, start_page: str, n: int = 1):
        ret = cls()
        ret.dfs(start_page, n)
        return ret

    def dfs(self, start_page: str, n: int = 1):
        """Run depth first search from the start page to a specified depth (n)
        """
        url = name_to_url(start_page)
        i = self.add_node(WikiNode(url, 0))
        stack = deque([i])
        while stack:
            nd = self.nodes[stack.pop()]
            if nd.level > n:
                continue
            nd.get_links()
            inter = set(self.node_map.keys()) & set(nd.out_paths)
            for link in nd.out_paths:
                if link not in self.node_map:
                    j = self.add_node(WikiNode(link, nd.level + 1))
                    stack.append(j)

    def add_node(self, node):
        if node.link not in self.node_map:
            idx = len(self.nodes)
            self.node_map[node.link] = idx
            self.nodes.append(node)

        return self.node_map[node.link]
