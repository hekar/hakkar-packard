import os
import subprocess
from pathlib import Path

import click
from metrum.common.logger import logger
from metrum.settings import settings

@click.command()
def init():
    """Initialize the Metrum environment."""
    logger.info("initializing_metrum_service")
    click.echo("Initializing Metrum service...")
    
    # Create necessary directories
    db_dir = Path("db")
    db_dir.mkdir(exist_ok=True)
    logger.debug("created_directory", path=str(db_dir))
    
    migrations_dir = db_dir / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    logger.debug("created_directory", path=str(migrations_dir))
    
    # Create logs directory if it doesn't exist
    logs_dir = settings.logs_dir
    logs_dir.mkdir(exist_ok=True, parents=True)
    logger.debug("created_directory", path=str(logs_dir))
    
    # Create cache directory if it doesn't exist
    cache_dir = Path(settings.patterns_cache_dir).expanduser()
    cache_dir.mkdir(exist_ok=True, parents=True)
    logger.debug("created_directory", path=str(cache_dir))
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        logger.info("creating_env_file")
        with env_file.open("w") as f:
            f.write(f"METRUM_DATABASE_URL={settings.database_url}\n")
            f.write("METRUM_HTTP_ENDPOINT=http://localhost:8000/events\n")  # Default value
            f.write("METRUM_BASE_URL=\n")
            f.write("METRUM_WS_URL=\n")
            f.write(f"METRUM_LOGS_DIR={settings.logs_dir}\n")
            f.write(f"METRUM_POLL_INTERVAL={settings.poll_interval}\n")
            f.write(f"METRUM_PATTERNS_CACHE_DIR={settings.patterns_cache_dir}\n")
            f.write("METRUM_PATTERNS_SOURCE=\n")  # Empty by default, will use built-in patterns
            f.write(f"METRUM_PATTERNS_CACHE_TTL={settings.patterns_cache_ttl}\n")
        logger.debug("created_env_file", path=str(env_file))
    else:
        logger.debug("env_file_exists", path=str(env_file))
    
    # Initialize dbmate
    dbmate_url = f"sqlite://{os.path.abspath('metrum.db')}"
    logger.debug("initializing_dbmate", url=dbmate_url)
    try:
        subprocess.run(["dbmate", "-u", dbmate_url, "init"], check=True)
        logger.info("dbmate_initialized")
    except subprocess.CalledProcessError as e:
        logger.error("dbmate_init_failed", error=str(e), exit_code=e.returncode)
        raise
    except FileNotFoundError:
        error_msg = "dbmate command not found. Please install dbmate first."
        logger.error("dbmate_not_found")
        click.echo(error_msg, err=True)
        return
    
    logger.info("metrum_initialized")
    click.echo("Metrum initialized successfully!") 