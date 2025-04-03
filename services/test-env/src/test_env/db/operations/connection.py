from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from test_env.settings import settings


def get_db_engine(db_name: str) -> Engine:
    """Create SQLAlchemy engine for the specified database.

    Args:
        db_name: Name of the database to connect to

    Returns:
        SQLAlchemy engine instance
    """
    return create_engine(
        f"postgresql://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{db_name}",
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def get_db_session(db_name: str) -> Session:
    """Create SQLAlchemy session for the specified database.

    Args:
        db_name: Name of the database to connect to

    Returns:
        SQLAlchemy session instance
    """
    engine = get_db_engine(db_name)
    SessionLocal = sessionmaker(engine, expire_on_commit=False)
    return SessionLocal()


@contextmanager
def get_connection(db_name: str = "postgres"):
    """Get raw connection for operations that need it."""
    engine = get_db_engine(db_name)
    with engine.connect() as conn:
        yield conn
