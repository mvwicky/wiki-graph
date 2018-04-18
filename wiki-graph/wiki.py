#! python3.6
import random
import time

from bs4 import BeautifulSoup

from graph import WikiGraph
from scrape import page_links, links_to_names


def generic_scrape():
    links = page_links('George_Washington')
    pg_names = links_to_names(links)
    all_links = set(links)
    for elem in pg_names:
        c = page_links(elem)
        all_links |= c
        print(len(c), len(all_links))
        time.sleep(random.randrange(5, 11))
    print(len(all_links))


def graph_test():
    # links = page_links('Counter-offensive')
    g = WikiGraph()
    start_time = time.perf_counter()
    g = WikiGraph.new_dfs('Federal_Digital_System', 1)
    end_time = time.perf_counter()
    print('DFS Time: {0:.4f}'.format(end_time - start_time))
    print(len(g.nodes), len(g.node_map))


def svg_soup(version=1.1, base_profile='full', width=300, height=300):
    soup = BeautifulSoup('<svg></svg>', 'lxml-xml')
    soup.svg.attrs.update({
        'version': version, 'baseProfile': base_profile,
        'width': width, 'height': height,
        'xmlns': 'http://www.w3.org/2000/svg'})
    return soup


def draw_graph(page_name, depth=1):
    graph = WikiGraph.new_dfs(page_name, depth)
    soup = svg_soup(
        width=(depth + 1) * 500, height=(len(graph.nodes) + 1) * 20)
    for i, node in enumerate(graph):
        nt = soup.new_tag('text')
        nt.attrs.update(**{
            'x': (node.level + 1) * 100,
            'y': (i + 1) * 15,
            'font-size': 12, 'text-anchor': 'inherit', 'fill': 'black'})
        nt.string = node.page_name.replace('_', ' ')
        soup.svg.append(nt)
    with open(page_name + '.svg', 'wt') as f:
        f.write(soup.prettify())


def adj_list(N=10):
    pass


if __name__ == '__main__':
    random.seed()
    draw_graph('Federal_Digital_System')
