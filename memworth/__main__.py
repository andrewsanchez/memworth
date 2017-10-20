import click

from memworth.record import Record


@click.command()
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    r = Record(path)
    r.extract_phrases()
