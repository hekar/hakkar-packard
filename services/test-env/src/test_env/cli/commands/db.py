import click
import logging
from test_env.db.operations import (
    create_database,
    drop_database,
    create_schema,
    populate_database,
    run_benchmark_queries,
)

logger = logging.getLogger(__name__)


@click.group(name="db")
@click.option("--model", "-m", default="default", help="Database model to use")
@click.pass_context
def db(ctx, model):
    """Database management commands."""
    ctx.ensure_object(dict)
    ctx.obj["model"] = model


@db.command(name="reset")
@click.pass_context
def reset_db(ctx):
    """Reset database (drop, create schema, and populate with 10MB of data)."""
    model = ctx.obj["model"]
    db_name = f"test_env_{model}"

    try:
        # Drop database if it exists
        click.echo(f"Dropping database {db_name} if it exists...")
        drop_database(db_name)

        # Create new database
        click.echo(f"Creating database {db_name}...")
        create_database(db_name)

        # Create schema
        click.echo("Creating database schema...")
        create_schema(db_name)

        # Populate with 10MB of data
        click.echo("Populating database with 10MB of data...")
        populate_database(db_name, 10)

        click.echo(f"Successfully reset database {db_name}!")
    except Exception as e:
        click.echo(f"Error resetting database: {str(e)}", err=True)


@db.command(name="populate")
@click.option(
    "--target-size",
    "-s",
    default=100,
    help="Target size in MB for the database population",
)
@click.pass_context
def populate_db(ctx, target_size):
    """Populate the database with random financial data."""
    model = ctx.obj["model"]
    db_name = f"test_env_{model}"

    try:
        click.echo(
            f"Populating database {db_name} with approximately {target_size}MB of data..."
        )
        populate_database(db_name, target_size)
        click.echo(
            f"Successfully populated database with approximately {target_size}MB of data!"
        )
    except Exception as e:
        click.echo(f"Error populating database: {str(e)}", err=True)


@db.command(name="bench")
@click.pass_context
def bench_db(ctx):
    """Run various complex queries to benchmark the database."""
    model = ctx.obj["model"]
    db_name = f"test_env_{model}"

    try:
        click.echo(f"Running benchmark queries on database {db_name}...")
        results = run_benchmark_queries(db_name)
        click.echo("\nBenchmark Results:")
        click.echo("-" * 50)
        for result in results:
            click.echo(f"\nQuery: {result['query']}")
            click.echo(f"Execution Time: {result['execution_time']:.4f} seconds")
            click.echo(f"Rows Returned: {result['row_count']}")
    except Exception as e:
        click.echo(f"Error running benchmark queries: {str(e)}", err=True)
