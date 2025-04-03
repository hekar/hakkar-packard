import asyncio
from datetime import datetime
from typing import Optional
from pathlib import Path
import click
import json
import os

import structlog

from metrum.logs import LogReader
from metrum.settings import settings
from metrum.common.logger import logger

logger = structlog.get_logger(__name__)

@click.group()
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
    logger.debug("reading_logs",
                follow=follow,
                since=since.isoformat() if since else None,
                until=until.isoformat() if until else None)

    if settings.log_mode != "filesystem":
        error_msg = f"Error: Log mode {settings.log_mode} not supported"
        logger.error("unsupported_log_mode", mode=settings.log_mode)
        click.echo(error_msg, err=True)
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

        logger.info("starting_log_reader", follow=follow)
        asyncio.run(read_logs())
    except FileNotFoundError as e:
        logger.error("file_not_found", error=str(e))
        click.echo(f"Error: {e}", err=True)
    except KeyboardInterrupt:
        logger.info("log_reading_stopped_by_user")
        click.echo("\nStopped reading logs")


@logs.command()
def list():
    """List available log files."""
    logger.debug("listing_log_files")
    reader = LogReader()
    try:
        log_files = reader.get_log_files()
        if not log_files:
            logger.info("no_log_files_found")
            click.echo("No log files found")
            return
        
        logger.info("found_log_files", count=len(log_files))
        click.echo("Available log files:")
        for log_file in log_files:
            size = log_file.stat().st_size
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            logger.debug("log_file_details",
                        name=log_file.name,
                        size=size,
                        modified=mtime.isoformat())
            click.echo(f"  {log_file.name} ({size/1024:.1f}KB, modified: {mtime})")
    except Exception as e:
        logger.error("error_listing_files", error=str(e), exc_info=True)
        click.echo(f"Error: {e}", err=True) 