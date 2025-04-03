from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from metrum.common.logger import logger
from metrum.settings import settings
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from metrum.db import Base

def setup_db_logging():
    """Setup database migration logging directory and return log file path."""
    log_dir = Path("/tmp/metrum")
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"db-{timestamp}.log"
    logger.debug("setup_db_logging", log_file=str(log_file))
    return log_file


def log_command_output(log_file: Path, command_name: str, output: str):
    """Log command output to file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a") as f:
        f.write(f"[{timestamp}] {command_name}:\n{output}\n\n")
    logger.debug("logged_command_output",
                log_file=str(log_file),
                command=command_name,
                output_length=len(output))


@click.group()
def db():
    """Manage the database."""
    pass


@db.command()
@click.option(
    "--count",
    type=int,
    help="Number of revisions to upgrade. If not provided, upgrades to the latest version."
)
def up(count: Optional[int] = None):
    """Upgrade the database schema.
    
    If count is provided, upgrades by that many revisions.
    Otherwise, upgrades to the latest version.
    """
    logger.info("upgrading_database", revision_count=count)
    log_file = setup_db_logging()
    alembic_cfg = Config("alembic.ini")
    
    try:
        if count is not None:
            logger.debug("upgrading_by_count", count=count)
            command.upgrade(alembic_cfg, f"+{count}")
            log_command_output(log_file, "up", f"Upgraded database by {count} revisions")
        else:
            logger.debug("upgrading_to_head")
            command.upgrade(alembic_cfg, "head")
            log_command_output(log_file, "up", "Upgraded database to latest version")
        logger.info("database_upgrade_complete")
    except Exception as e:
        logger.error("database_upgrade_failed", error=str(e), exc_info=True)
        log_command_output(log_file, "up", f"Error: {str(e)}")
        raise


@db.command()
@click.option(
    "--count",
    type=int,
    help="Number of revisions to rollback. If not provided, rolls back to the first version."
)
def rollback(count: Optional[int] = None):
    """Rollback the database schema.
    
    If count is provided, rolls back by that many revisions.
    Otherwise, rolls back to the first version.
    """
    logger.info("rolling_back_database", revision_count=count)
    log_file = setup_db_logging()
    alembic_cfg = Config("alembic.ini")
    
    try:
        if count is not None:
            logger.debug("rolling_back_by_count", count=count)
            command.downgrade(alembic_cfg, f"-{count}")
            log_command_output(log_file, "rollback", f"Rolled back database by {count} revisions")
        else:
            logger.debug("rolling_back_to_base")
            command.downgrade(alembic_cfg, "base")
            log_command_output(log_file, "rollback", "Rolled back database to first version")
        logger.info("database_rollback_complete")
    except Exception as e:
        logger.error("database_rollback_failed", error=str(e), exc_info=True)
        log_command_output(log_file, "rollback", f"Error: {str(e)}")
        raise


@db.command()
def reset():
    """Reset the database by dropping all tables and running migrations from scratch."""
    log_file = setup_db_logging()
    
    if click.confirm("This will delete all data in the database. Are you sure?"):
        try:
            # Drop all tables
            engine = create_engine(settings.database_url)
            Base.metadata.drop_all(engine)
            log_command_output(log_file, "reset", "Dropped all tables")
            
            # Run migrations to latest version
            alembic_cfg = Config("alembic.ini")
            command.upgrade(alembic_cfg, "head")
            log_command_output(log_file, "reset", "Applied all migrations")
            
            click.echo("Database has been reset and migrations have been applied.")
        except Exception as e:
            log_command_output(log_file, "reset", f"Error: {str(e)}")
            raise 