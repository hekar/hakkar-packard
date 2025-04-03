from typing import List
from sqlalchemy import text, create_engine
from .connection import get_connection


def get_databases() -> List[str]:
    """Get list of databases."""
    with get_connection() as conn:
        result = conn.execute(
            text(
                """
            SELECT datname 
            FROM pg_database 
            WHERE datistemplate = false 
            AND datname != 'postgres'
            ORDER BY datname;
        """
            )
        )
        return [row[0] for row in result]


def create_database(name: str):
    """Create a new database."""
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5433/postgres",
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {name};"))


def drop_database(name: str):
    """Drop a database."""
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5433/postgres",
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as conn:
        # Terminate all connections to the database
        conn.execute(
            text(
                """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = :name
            AND pid <> pg_backend_pid();
        """
            ),
            {"name": name},
        )
        conn.execute(text(f"DROP DATABASE IF EXISTS {name};"))


def get_database_size(db_name: str) -> float:
    """Get the size of a database in megabytes.

    Args:
        db_name: Name of the database

    Returns:
        Size of the database in megabytes
    """
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5433/postgres",
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
            SELECT pg_database_size(:db_name) / (1024 * 1024) as size_mb
            """
            ),
            {"db_name": db_name},
        )
        return result.scalar()
