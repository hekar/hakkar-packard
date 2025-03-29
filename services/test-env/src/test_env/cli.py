import click
import structlog
import asyncio
from functools import wraps
from .db import create_schema, populate_database, run_benchmark_queries

logger = structlog.get_logger()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def main():
    """test-env CLI application."""
    pass


@main.command()
@coro
async def migrate_db():
    """Create the database schema with complex financial tables and views."""
    try:
        logger.info("migrating schema")
        await create_schema()
        click.echo("Successfully created database schema!")
    except Exception as e:
        click.echo(f"Error creating database schema: {str(e)}", err=True)


@main.command()
@coro
@click.option(
    "--size", "-s", default=100, help="Target size in MB for the database population"
)
async def populate_db(size):
    """Populate the database with random financial data."""
    try:
        await populate_database(size)
        click.echo(
            f"Successfully populated database with approximately {size}MB of data!"
        )
    except Exception as e:
        click.echo(f"Error populating database: {str(e)}", err=True)


@main.command()
@coro
async def bench_db():
    """Run various complex queries to benchmark the database."""
    try:
        results = await run_benchmark_queries()
        click.echo("\nBenchmark Results:")
        click.echo("-" * 50)
        for result in results:
            click.echo(f"\nQuery: {result['query']}")
            click.echo(f"Execution Time: {result['execution_time']:.4f} seconds")
            click.echo(f"Rows Returned: {result['row_count']}")
    except Exception as e:
        click.echo(f"Error running benchmark queries: {str(e)}", err=True)


if __name__ == "__main__":
    main()
