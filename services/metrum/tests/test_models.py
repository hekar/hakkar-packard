from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy import select

from metrum.db import EventQueue, EventStatus


def test_create_event(db_session, sample_event):
    """Test creating a new event."""
    event = EventQueue(
        event_type=sample_event["event_type"],
        payload=sample_event["payload"],
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    assert event.id is not None
    assert event.event_type == sample_event["event_type"]
    assert event.payload == sample_event["payload"]
    assert event.status == EventStatus.PENDING
    assert isinstance(event.created_at, datetime)
    assert isinstance(event.updated_at, datetime)
    assert event.processed_at is None
    assert event.error_message is None


def test_update_event_status(db_session, event_in_db):
    """Test updating event status."""
    # Record the current updated_at timestamp
    original_updated_at = event_in_db.updated_at

    # Wait a small amount to ensure the timestamp will be different
    with patch('metrum.db.datetime') as mock_datetime:
        # Set a fixed time for the test
        mock_now = datetime.utcnow() + timedelta(seconds=1)
        mock_datetime.utcnow.return_value = mock_now
        
        # Update the status
        event_in_db.status = EventStatus.PROCESSING
        db_session.commit()
        db_session.refresh(event_in_db)

    assert event_in_db.status == EventStatus.PROCESSING
    assert event_in_db.updated_at > original_updated_at


def test_complete_event_processing(db_session, event_in_db):
    """Test completing event processing."""
    with patch('metrum.db.datetime') as mock_datetime:
        mock_now = datetime.utcnow()
        mock_datetime.utcnow.return_value = mock_now
        
        # Update event to completed
        event_in_db.status = EventStatus.COMPLETED
        event_in_db.processed_at = mock_now
        db_session.commit()
        db_session.refresh(event_in_db)

    assert event_in_db.status == EventStatus.COMPLETED
    assert event_in_db.processed_at == mock_now
    assert event_in_db.error_message is None


def test_failed_event_processing(db_session, event_in_db):
    """Test failed event processing."""
    error_message = "Test error message"
    
    with patch('metrum.db.datetime') as mock_datetime:
        mock_now = datetime.utcnow()
        mock_datetime.utcnow.return_value = mock_now
        
        # Update event to failed
        event_in_db.status = EventStatus.FAILED
        event_in_db.error_message = error_message
        event_in_db.processed_at = mock_now
        db_session.commit()
        db_session.refresh(event_in_db)

    assert event_in_db.status == EventStatus.FAILED
    assert event_in_db.processed_at == mock_now
    assert event_in_db.error_message == error_message


def test_query_events_by_status(db_session, event_in_db):
    """Test querying events by status."""
    # Create additional events with different statuses
    events = [
        EventQueue(
            event_type="test_event",
            payload={"test": f"data_{i}"},
            status=status
        )
        for i, status in enumerate([
            EventStatus.PENDING,
            EventStatus.PROCESSING,
            EventStatus.COMPLETED,
            EventStatus.FAILED
        ])
    ]
    db_session.add_all(events)
    db_session.commit()

    # Query events by each status
    for status in EventStatus:
        stmt = select(EventQueue).where(EventQueue.status == status)
        result = db_session.execute(stmt).scalars().all()
        assert len(result) == 1
        assert all(event.status == status for event in result)


def test_event_validation(db_session):
    """Test event validation and constraints."""
    # Test missing required fields
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        event = EventQueue(payload={"test": "data"})  # Missing event_type
        db_session.add(event)
        db_session.commit()

    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        event = EventQueue(event_type="test_event")  # Missing payload
        db_session.add(event)
        db_session.commit()


def test_json_payload_handling(db_session):
    """Test handling of JSON payloads."""
    # Test different JSON payload types
    payloads = [
        {"string": "value"},
        {"number": 123},
        {"boolean": True},
        {"null": None},
        {"array": [1, 2, 3]},
        {"nested": {"key": "value"}},
        [1, 2, 3],  # Array as root
        "string",    # String as root
        123,        # Number as root
        True,       # Boolean as root
    ]

    for payload in payloads:
        event = EventQueue(
            event_type="test_event",
            payload=payload
        )
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        assert event.payload == payload 