from datetime import datetime
from uuid import uuid4
import pandas as pd
import numpy as np
from sqlalchemy import (
    Column,
    String,
    Numeric,
    ForeignKey,
    DateTime,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from io import StringIO

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    accounts = relationship("Account", back_populates="customer")

    @classmethod
    def generate_test_data(cls, num_rows: int) -> pd.DataFrame:
        """Generate test data for customers."""
        return pd.DataFrame(
            {
                "customer_id": [str(uuid4()) for _ in range(num_rows)],
                "first_name": [f"Customer{i}" for i in range(num_rows)],
                "last_name": [f"Last{i}" for i in range(num_rows)],
                "created_at": [datetime.utcnow() for _ in range(num_rows)],
            }
        )

    @classmethod
    def truncate(cls, session):
        """Truncate the customers table."""
        session.execute(text("TRUNCATE TABLE customers CASCADE"))
        session.commit()

    @classmethod
    def bulk_insert(cls, session, df: pd.DataFrame):
        """Bulk insert customers using COPY command."""
        conn = session.get_bind().raw_connection()
        try:
            with conn.cursor() as cur:
                output = StringIO()
                df.to_csv(output, index=False, header=False)
                output.seek(0)
                cur.copy_expert(
                    "COPY customers (customer_id, first_name, last_name, created_at) FROM STDIN WITH CSV",
                    output,
                )
            conn.commit()
        finally:
            conn.close()


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"))
    balance = Column(Numeric(15, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    investments = relationship("Investment", back_populates="account")

    @classmethod
    def generate_test_data(cls, num_rows: int, customer_ids: list) -> pd.DataFrame:
        """Generate test data for accounts."""
        df = pd.DataFrame(
            {
                "account_id": [str(uuid4()) for _ in range(num_rows)],
                "customer_id": np.random.choice(
                    customer_ids, size=num_rows, replace=True
                ),
                "balance": np.random.uniform(0, 10000, num_rows),
                "created_at": [datetime.utcnow() for _ in range(num_rows)],
            }
        )
        return df

    @classmethod
    def truncate(cls, session):
        """Truncate the accounts table."""
        session.execute(text("TRUNCATE TABLE accounts CASCADE"))
        session.commit()

    @classmethod
    def bulk_insert(cls, session, df: pd.DataFrame):
        """Bulk insert accounts using COPY command."""
        conn = session.get_bind().raw_connection()
        try:
            with conn.cursor() as cur:
                output = StringIO()
                df.to_csv(output, index=False, header=False)
                output.seek(0)
                cur.copy_expert(
                    "COPY accounts (account_id, customer_id, balance, created_at) FROM STDIN WITH CSV",
                    output,
                )
            conn.commit()
        finally:
            conn.close()


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"))
    transaction_type = Column(String, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    account = relationship("Account", back_populates="transactions")

    @classmethod
    def generate_test_data(cls, num_rows: int, account_ids: list) -> pd.DataFrame:
        """Generate test data for transactions."""
        df = pd.DataFrame(
            {
                "transaction_id": [str(uuid4()) for _ in range(num_rows)],
                "account_id": np.random.choice(
                    account_ids, size=num_rows, replace=True
                ),
                "transaction_type": np.random.choice(
                    ["deposit", "withdrawal"], size=num_rows
                ),
                "amount": np.random.uniform(0, 1000, num_rows),
                "created_at": [datetime.utcnow() for _ in range(num_rows)],
            }
        )
        return df

    @classmethod
    def truncate(cls, session):
        """Truncate the transactions table."""
        session.execute(text("TRUNCATE TABLE transactions CASCADE"))
        session.commit()

    @classmethod
    def bulk_insert(cls, session, df: pd.DataFrame):
        """Bulk insert transactions using COPY command."""
        conn = session.get_bind().raw_connection()
        try:
            with conn.cursor() as cur:
                output = StringIO()
                df.to_csv(output, index=False, header=False)
                output.seek(0)
                cur.copy_expert(
                    "COPY transactions (transaction_id, account_id, transaction_type, amount, created_at) FROM STDIN WITH CSV",
                    output,
                )
            conn.commit()
        finally:
            conn.close()


class Investment(Base):
    __tablename__ = "investments"

    investment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"))
    amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    account = relationship("Account", back_populates="investments")

    @classmethod
    def generate_test_data(cls, num_rows: int, account_ids: list) -> pd.DataFrame:
        """Generate test data for investments."""
        df = pd.DataFrame(
            {
                "investment_id": [str(uuid4()) for _ in range(num_rows)],
                "account_id": np.random.choice(
                    account_ids, size=num_rows, replace=True
                ),
                "amount": np.random.uniform(0, 5000, num_rows),
                "created_at": [datetime.utcnow() for _ in range(num_rows)],
            }
        )
        return df

    @classmethod
    def truncate(cls, session):
        """Truncate the investments table."""
        session.execute(text("TRUNCATE TABLE investments CASCADE"))
        session.commit()

    @classmethod
    def bulk_insert(cls, session, df: pd.DataFrame):
        """Bulk insert investments using COPY command."""
        conn = session.get_bind().raw_connection()
        try:
            with conn.cursor() as cur:
                output = StringIO()
                df.to_csv(output, index=False, header=False)
                output.seek(0)
                cur.copy_expert(
                    "COPY investments (investment_id, account_id, amount, created_at) FROM STDIN WITH CSV",
                    output,
                )
            conn.commit()
        finally:
            conn.close()
