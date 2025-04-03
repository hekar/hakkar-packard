import click

from .cli_db import db
from .cli_run import run
from .cli_init import init
from .cli_logs import logs


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