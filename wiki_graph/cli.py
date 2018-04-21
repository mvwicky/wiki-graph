import click

from wiki_graph.scrape import WikiPage
# from wiki_graph.graph import WikiGraph


@click.group()
def cli():
    pass


@click.command()
@click.argument('pagename')
@click.option('--method', default='dfs', type=click.Choice(['dfs', 'bfs']))
@click.option('--depth', default=1)
def search(pagename, method, depth):
    click.secho(pagename, fg='red')
    # g = WikiGraph.new(method, pagename, depth)
    # click.echo(repr(g))


@click.command()
@click.argument('pagename')
def links(pagename):
    click.secho(pagename, fg='red')
    # w = WikiPageLinks('Bicameralism_(psychology)')
    w = WikiPage(pagename)
    for link in w.absolute_links:
        click.echo(link)
    click.echo(len(w.links))
    click.echo(repr(w))
    click.echo(w.title)


cli.add_command(search)
cli.add_command(links)
