import click

from wiki_graph.graph import WikiGraph


@click.command()
@click.argument('pagename')
@click.option('--method', default='dfs', type=click.Choice(['dfs', 'bfs']))
@click.option('--depth', default=1)
def cli(pagename, method, depth):
    click.secho(pagename, fg='red')
    g = WikiGraph.new(method, pagename, depth)
    click.echo(repr(g))
