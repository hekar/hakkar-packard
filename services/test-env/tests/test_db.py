import pytest
import uuid
from test_env.db import (
    populate_database,
    run_benchmark_queries,
    get_customer_portfolio,
    get_transaction_analytics,
)


@pytest.mark.asyncio
@pytest.mark.uses_testcontainer
async def test_schema_creation(db_connection):
    """Test that schema creation works correctly."""
    # Verify tables exist
    tables = await db_connection.fetch(
        """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    """
    )
    table_names = {row["table_name"] for row in tables}

    expected_tables = {"customers", "accounts", "transactions", "investments"}
    assert expected_tables.issubset(
        table_names
    ), f"Missing tables. Found: {table_names}"


@pytest.mark.asyncio
@pytest.mark.uses_testcontainer
async def test_data_population(db_connection):
    """Test that data population works correctly."""
    # Populate with minimal data for testing
    await populate_database(target_size_mb=1)

    # Verify data was populated
    customer_count = await db_connection.fetchval("SELECT COUNT(*) FROM customers")
    account_count = await db_connection.fetchval("SELECT COUNT(*) FROM accounts")
    transaction_count = await db_connection.fetchval(
        "SELECT COUNT(*) FROM transactions"
    )
    investment_count = await db_connection.fetchval("SELECT COUNT(*) FROM investments")

    assert customer_count > 0, "No customers were created"
    assert account_count > 0, "No accounts were created"
    assert transaction_count > 0, "No transactions were created"
    assert investment_count > 0, "No investments were created"


@pytest.mark.asyncio
@pytest.mark.uses_testcontainer
async def test_benchmark_queries(db_connection):
    """Test that benchmark queries execute successfully."""
    # Run benchmark queries
    await run_benchmark_queries()

    # Verify queries executed successfully by checking for data
    customer_count = await db_connection.fetchval("SELECT COUNT(*) FROM customers")
    assert customer_count > 0, "Benchmark queries failed to execute"


@pytest.mark.asyncio
@pytest.mark.uses_testcontainer
async def test_customer_portfolio_view(db_connection):
    """Test that customer portfolio view works correctly."""
    # Insert test data
    customer_id = uuid.uuid4()
    await db_connection.execute(
        """
        INSERT INTO customers (customer_id, first_name, last_name)
        VALUES ($1, 'Test', 'User')
    """,
        customer_id,
    )

    account_id = uuid.uuid4()
    await db_connection.execute(
        """
        INSERT INTO accounts (account_id, customer_id, balance)
        VALUES ($1, $2, 1000.00)
    """,
        account_id,
        customer_id,
    )

    await db_connection.execute(
        """
        INSERT INTO investments (investment_id, account_id, amount)
        VALUES ($1, $2, 500.00)
    """,
        uuid.uuid4(),
        account_id,
    )

    # Get customer portfolio
    portfolio = await get_customer_portfolio(str(customer_id))

    # Verify portfolio data
    assert portfolio is not None, "Portfolio not found"
    assert str(portfolio["customer_id"]) == str(customer_id)
    assert float(portfolio["total_balance"]) == 1000.0
    assert float(portfolio["total_investments"]) == 500.0


@pytest.mark.asyncio
@pytest.mark.uses_testcontainer
async def test_transaction_analytics_view(db_connection):
    """Test that transaction analytics view works correctly."""
    # Clean existing data
    await db_connection.execute("TRUNCATE TABLE transactions CASCADE")

    # Insert test data
    customer_id = uuid.uuid4()
    await db_connection.execute(
        """
        INSERT INTO customers (customer_id, first_name, last_name)
        VALUES ($1, 'Test', 'User')
    """,
        customer_id,
    )

    account_id = uuid.uuid4()
    await db_connection.execute(
        """
        INSERT INTO accounts (account_id, customer_id, balance)
        VALUES ($1, $2, 1000.00)
    """,
        account_id,
        customer_id,
    )

    # Insert test transactions
    await db_connection.execute(
        """
        INSERT INTO transactions (transaction_id, account_id, transaction_type, amount)
        VALUES ($1, $2, 'deposit', 1000.00)
    """,
        uuid.uuid4(),
        account_id,
    )

    await db_connection.execute(
        """
        INSERT INTO transactions (transaction_id, account_id, transaction_type, amount)
        VALUES ($1, $2, 'withdrawal', 500.00)
    """,
        uuid.uuid4(),
        account_id,
    )

    # Get transaction analytics
    analytics = await get_transaction_analytics()

    # Verify analytics data
    assert len(analytics) == 2, "Expected two transaction types"
    deposit = next(t for t in analytics if t["transaction_type"] == "deposit")
    withdrawal = next(t for t in analytics if t["transaction_type"] == "withdrawal")

    assert deposit["count"] == 1, "Expected one deposit"
    assert withdrawal["count"] == 1, "Expected one withdrawal"
    assert float(deposit["total_amount"]) == 1000.0, "Incorrect deposit amount"
    assert float(withdrawal["total_amount"]) == 500.0, "Incorrect withdrawal amount"
