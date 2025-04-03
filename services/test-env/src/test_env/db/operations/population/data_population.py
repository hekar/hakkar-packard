import logging
import pandas as pd
import numpy as np
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session
from test_env.db.models import Customer, Account, Transaction, Investment
from ..connection import get_db_engine
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_dataframe(num_rows: int, columns: dict) -> pd.DataFrame:
    """Generate a pandas DataFrame with random data based on column specifications."""
    data = {}
    for col, spec in columns.items():
        if spec["type"] == "uuid":
            data[col] = [str(uuid4()) for _ in range(num_rows)]
        elif spec["type"] == "string":
            data[col] = [f"{spec['prefix']}{i}" for i in range(num_rows)]
        elif spec["type"] == "numeric":
            data[col] = np.random.uniform(spec["min"], spec["max"], num_rows)
        elif spec["type"] == "datetime":
            data[col] = [datetime.utcnow() for _ in range(num_rows)]
    return pd.DataFrame(data)


def populate_database(db_name: str, target_size_mb: int = 100):
    """Populate database with test data until reaching target size using pandas and COPY.

    Args:
        db_name: Name of the database to populate
        target_size_mb: Target database size in megabytes
    """
    engine = get_db_engine(db_name)
    batch_size = 10000  # Number of records per batch

    with Session(engine) as session:
        logger.info(f"Populating database {db_name}...")
        batch_count = 0

        while True:
            batch_count += 1
            logger.debug(f"Starting batch {batch_count} for {db_name}")

            # Generate and insert customers
            logger.debug("Generating customers...")
            customers_df = Customer.generate_test_data(batch_size)
            if batch_count == 1:
                Customer.truncate(session)
            Customer.bulk_insert(session, customers_df)

            # Generate and insert accounts
            logger.debug("Generating accounts...")
            accounts_df = Account.generate_test_data(
                batch_size * 2, customers_df["customer_id"].tolist()
            )
            if batch_count == 1:
                Account.truncate(session)
            Account.bulk_insert(session, accounts_df)

            # Generate and insert transactions
            logger.debug("Generating transactions...")
            transactions_df = Transaction.generate_test_data(
                batch_size * 5, accounts_df["account_id"].tolist()
            )
            if batch_count == 1:
                Transaction.truncate(session)
            Transaction.bulk_insert(session, transactions_df)

            # Generate and insert investments
            logger.debug("Generating investments...")
            investments_df = Investment.generate_test_data(
                batch_size, accounts_df["account_id"].tolist()
            )
            if batch_count == 1:
                Investment.truncate(session)
            Investment.bulk_insert(session, investments_df)

            # Get current database size
            logger.debug("Checking database size...")
            result = session.execute(
                text("SELECT pg_database_size(current_database()) / (1024 * 1024)")
            )
            current_size = result.scalar()

            # Log progress
            logger.info(
                f"Batch {batch_count}: Current database size: {current_size:.2f}MB / Target: {target_size_mb}MB"
            )

            if current_size >= target_size_mb:
                logger.info(f"Target size reached: {current_size:.2f}MB")
                break
