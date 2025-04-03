from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.orm import Session

from metrum.db import get_db


def test_get_db():
    """Test the database session context manager."""
    mock_session = MagicMock(spec=Session)
    mock_session_local = MagicMock(return_value=mock_session)

    with patch("metrum.db.SessionLocal", mock_session_local):
        db_generator = get_db()
        db = next(db_generator)

        # Test that we got the session
        assert db == mock_session

        # Test that close is called when the generator is closed
        try:
            next(db_generator)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()


def test_get_db_with_exception():
    """Test the database session context manager when an exception occurs."""
    mock_session = MagicMock(spec=Session)
    mock_session_local = MagicMock(return_value=mock_session)

    with patch("metrum.db.SessionLocal", mock_session_local):
        db_generator = get_db()
        next(db_generator)

        # Simulate an exception
        with pytest.raises(Exception):
            with patch.object(
                mock_session, "close", side_effect=Exception("Test error")
            ):
                try:
                    next(db_generator)
                except StopIteration:
                    pass
                raise Exception("Test error")

        # Verify close was attempted
        mock_session.close.assert_called_once()

