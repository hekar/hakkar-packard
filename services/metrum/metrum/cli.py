import asyncio
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import click

from .logs import LogReader
from .settings import settings


@click.group()
def cli():
    """Metrum CLI tool."""
    pass


@cli.command()
def init():
    """Initialize the Metrum environment."""
    click.echo("Initializing Metrum...")
    
    # Create necessary directories
    db_dir = Path("db")
    db_dir.mkdir(exist_ok=True)
    
    migrations_dir = db_dir / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    
    # Create logs directory if it doesn't exist
    logs_dir = settings.logs_dir
    logs_dir.mkdir(exist_ok=True, parents=True)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        with env_file.open("w") as f:
            f.write(f"METRUM_DATABASE_URL={settings.database_url}\n")
            f.write("METRUM_BASE_URL=\n")
            f.write("METRUM_WS_URL=\n")
            f.write(f"METRUM_LOGS_DIR={settings.logs_dir}\n")
    
    # Initialize dbmate
    dbmate_url = f"sqlite://{os.path.abspath('metrum.db')}"
    subprocess.run(["dbmate", "-u", dbmate_url, "init"], check=True)
    
    click.echo("Metrum initialized successfully!")


@cli.command()
def run():
    """Run the Metrum service."""
    click.echo("Starting Metrum service...")
    # Add your service running logic here
    click.echo("Metrum service is running!")


@cli.group()
def logs():
    """Manage and read PostgreSQL logs."""
    pass


@logs.command()
@click.option(
    "--follow", "-f",
    is_flag=True,
    help="Follow log file in real-time"
)
@click.option(
    "--since",
    type=click.DateTime(),
    help="Show logs since timestamp (format: YYYY-MM-DD HH:MM:SS)"
)
@click.option(
    "--until",
    type=click.DateTime(),
    help="Show logs until timestamp (format: YYYY-MM-DD HH:MM:SS)"
)
def read(
    follow: bool = False,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None
):
    """Read PostgreSQL logs."""
    if settings.log_mode != "filesystem":
        click.echo(f"Error: Log mode {settings.log_mode} not supported", err=True)
        return

    reader = LogReader()
    
    try:
        # Run the async log reader in the event loop
        async def read_logs():
            async for line in reader.read_logs(
                follow=follow,
                start_time=since,
                end_time=until
            ):
                click.echo(line)

        asyncio.run(read_logs())
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
    except KeyboardInterrupt:
        click.echo("\nStopped reading logs")


@logs.command()
def list():
    """List available log files."""
    reader = LogReader()
    try:
        log_files = reader.get_log_files()
        if not log_files:
            click.echo("No log files found")
            return
        
        click.echo("Available log files:")
        for log_file in log_files:
            size = log_file.stat().st_size
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            click.echo(f"  {log_file.name} ({size/1024:.1f}KB, modified: {mtime})")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli() 