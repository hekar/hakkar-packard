import click
from .core import example_function
from .db import create_schema, populate_database, run_benchmark_queries

@click.group()
def main():
    """test-env CLI application."""
    pass

@main.command()
@click.option('--name', '-n', default='World',
              help='Name to greet')
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name}!")

@main.command()
def example():
    """Run an example function."""
    result = example_function()
    click.echo(f"Example function result: {result}")

@main.command()
def migrate_db():
    """Create the database schema with complex financial tables and views."""
    try:
        create_schema()
        click.echo("Successfully created database schema!")
    except Exception as e:
        click.echo(f"Error creating database schema: {str(e)}", err=True)

@main.command()
@click.option('--size', '-s', default=100,
              help='Target size in MB for the database population')
def populate_db(size):
    """Populate the database with random financial data."""
    try:
        populate_database(size)
        click.echo(f"Successfully populated database with approximately {size}MB of data!")
    except Exception as e:
        click.echo(f"Error populating database: {str(e)}", err=True)

@main.command()
def bench_db():
    """Run various complex queries to benchmark the database."""
    try:
        results = run_benchmark_queries()
        click.echo("\nBenchmark Results:")
        click.echo("-" * 50)
        for result in results:
            click.echo(f"\nQuery: {result['query']}")
            click.echo(f"Execution Time: {result['execution_time']:.4f} seconds")
            click.echo(f"Rows Returned: {result['row_count']}")
    except Exception as e:
        click.echo(f"Error running benchmark queries: {str(e)}", err=True)

if __name__ == '__main__':
    main() 