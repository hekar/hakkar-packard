import click
import logging
from test_env.db.operations import get_databases

logger = logging.getLogger(__name__)


@click.command(name="list")
def list_databases():
    """List all available databases."""
    try:
        databases = get_databases()
        if not databases:
            click.echo("No databases found.")
            return

        click.echo("Available databases:")
        for db in databases:
            click.echo(f"  - {db}")
    except Exception as e:
        click.echo(f"Error listing databases: {str(e)}", err=True)
