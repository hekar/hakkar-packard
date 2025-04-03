from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from test_env.settings import settings

# Create engine
engine = create_engine(
    f"postgresql://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.database}",
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
)


def get_session() -> Session:
    """Get a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
