import os
from collections import deque
from typing import List, ClassVar, Union

import attr

from wiki_graph.scrape import name_to_url
from wiki_graph.node import WikiNode


class GraphTypeError(Exception):
    pass


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
            raise NotImplementedError('What is {0!r}?'.format(type(item)))

    def __iter__(self):
        return iter(self.nodes)

    def __repr__(self):
        if self.nodes:
            return '<WikiGraph: {0}>'.format(self.nodes[0])
        else:
            return '<WikiGraph: No Nodes>'

    @classmethod
    def new(cls, method: str, start_page: str, n: int = 1):
        method = method.lower()
        if method not in ('dfs', 'bfs'):
            raise GraphTypeError(
                '"method" must be "dfs" or "bfs" (got {0})'.format(method)
            )
        ret = cls()
        if method.startswith('dfs'):
            ret.depth_first_search(start_page, n)
        elif method.startswith('bfs'):
            ret.breadth_first_search(start_page, n)

    @classmethod
    def new_dfs(cls, start_page: str, n: int = 1):
        ret = cls()
        ret.depth_first_search(start_page, n)
        return ret

    def breadth_first_search(self, start_page: str, n: int = 1):
        url = name_to_url(start_page)
        i = self.add_node(WikiNode(url, 0))
        queue = deque()
        queue.append(i)
        while queue:
            nd = self.nodes[queue.popleft()]
            if nd.level > n:
                continue

            nd.get_links()
            # inter = set(self.node_map.keys()) & set(nd.out_paths)
            for link in nd.out_paths:
                if link in self.node_map:
                    continue

                j = self.add_node(WikiNode(link, nd.level + 1))
                queue.append(j)

    def depth_first_search(self, start_page: str, n: int = 1):
        """Run depth first search from the start page to a specified depth (n)
        """
        url = name_to_url(start_page)
        i = self.add_node(WikiNode(url, 0))
        stack = deque()
        stack.append(i)
        while stack:
            nd = self.nodes[stack.pop()]
            if nd.level > n:
                continue

            nd.get_links()
            # inter = set(self.node_map.keys()) & set(nd.out_paths)
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
