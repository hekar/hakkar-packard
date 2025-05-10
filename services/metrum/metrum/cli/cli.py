import click

from metrum.cli.cli_db import db
from metrum.cli.cli_run import run
from metrum.cli.cli_init import init
from metrum.cli.cli_logs import logs


@click.group()
def cli():
    """Metrum CLI tool."""
    pass


cli.add_command(init)
cli.add_command(db)
cli.add_command(run)
cli.add_command(logs)


if __name__ == "__main__":
    cli() 
