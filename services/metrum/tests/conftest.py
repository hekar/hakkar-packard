import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from metrum.db import Base, EventQueue


@pytest.fixture(scope="session")
def test_db_url():
    """Get test database URL."""
    return "sqlite:///./test.db"


@pytest.fixture(scope="session")
def engine(test_db_url):
    """Create test database engine."""
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def db_session(engine):
    """Create a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def sample_event():
    """Create a sample event for testing."""
    return {
        "event_type": "test_event",
        "payload": {"test": "data"},
    }


@pytest.fixture
def event_in_db(db_session, sample_event):
    """Create a sample event in the database."""
    event = EventQueue(
        event_type=sample_event["event_type"],
        payload=sample_event["payload"],
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event 