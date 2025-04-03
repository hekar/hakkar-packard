import logging
from sqlalchemy.orm import Session
from test_env.db.models import Base
from test_env.db.views import create_views
from ..connection import get_db_engine

logger = logging.getLogger(__name__)


def create_schema(db_name: str):
    """Create database schema using SQLAlchemy.

    Args:
        db_name: Name of the database to create schema in
    """
    try:
        engine = get_db_engine(db_name)
        with Session(engine) as session:
            # Create all tables using SQLAlchemy's create_all
            Base.metadata.create_all(engine)
            logger.info(f"Successfully created all database tables in {db_name}")

            # Create views after tables are created
            create_views(session)
            logger.info(f"Successfully created database views in {db_name}")

    except Exception as e:
        logger.error(f"Failed to create schema in {db_name}: {e}")
        raise
