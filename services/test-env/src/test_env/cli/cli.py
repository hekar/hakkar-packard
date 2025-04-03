import click
import logging
from .commands.db import db
from .commands.list import list_databases

logger = logging.getLogger(__name__)


@click.group()
def main():
    """test-env CLI application."""
    pass


# Register command groups
main.add_command(db)
main.add_command(list_databases)


if __name__ == "__main__":
    main()
