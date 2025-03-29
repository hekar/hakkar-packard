import pytest
from unittest.mock import call
from datetime import datetime
import uuid
from test_env.models import Customer, Account, Transaction, Investment


@pytest.mark.asyncio
async def test_customer_creation(db_connection):
    """Test customer creation logic."""
    customer_id = str(uuid.uuid4())
    db_connection.execute.return_value = None
    db_connection.fetchrow.return_value = {
        "customer_id": customer_id,
        "first_name": "Test",
        "last_name": "User",
        "created_at": datetime.now(),
    }

    # Test customer creation
    await Customer.create(db_connection, first_name="Test", last_name="User")
    db_connection.execute.assert_called_once()


@pytest.mark.asyncio
async def test_account_balance_update(db_connection):
    """Test account balance update logic."""
    account_id = str(uuid.uuid4())
    initial_balance = 1000.00
    deposit_amount = 500.00

    db_connection.fetchrow.return_value = {
        "account_id": account_id,
        "balance": initial_balance + deposit_amount,
    }

    # Test balance update
    account = Account(account_id=account_id, balance=initial_balance)
    await account.update_balance(db_connection, deposit_amount)

    db_connection.execute.assert_called_once()
    assert account.balance == initial_balance + deposit_amount


@pytest.mark.asyncio
async def test_transaction_validation(db_connection):
    """Test transaction validation logic."""
    account_id = str(uuid.uuid4())

    # Test withdrawal validation with insufficient funds
    account = Account(account_id=account_id, balance=100.00)
    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        account_id=account_id,
        transaction_type="WITHDRAWAL",
        amount=200.00,
    )

    with pytest.raises(ValueError, match="Insufficient funds"):
        await transaction.validate(db_connection, account)


@pytest.mark.asyncio
async def test_investment_allocation(db_connection):
    """Test investment allocation logic."""
    account_id = str(uuid.uuid4())
    investment_amount = 500.00

    db_connection.fetchrow.return_value = {"account_id": account_id, "balance": 1000.00}

    # Test investment creation
    investment = Investment(
        investment_id=str(uuid.uuid4()), account_id=account_id, amount=investment_amount
    )

    await investment.allocate(db_connection)

    # Verify both the investment creation and balance update calls
    assert db_connection.execute.call_count == 2
    db_connection.execute.assert_has_calls(
        [
            call(
                """
            INSERT INTO investments (investment_id, account_id, amount)
            VALUES ($1, $2, $3)
            """,
                investment.investment_id,
                account_id,
                investment_amount,
            ),
            call(
                """
            UPDATE accounts 
            SET balance = balance - $2
            WHERE account_id = $1
            """,
                account_id,
                investment_amount,
            ),
        ]
    )


@pytest.mark.asyncio
async def test_customer_portfolio_calculation(db_connection):
    """Test customer portfolio calculation logic."""
    customer_id = str(uuid.uuid4())

    # Mock portfolio data
    db_connection.fetchrow.return_value = {
        "total_balance": 5000.00,
        "total_investments": 3,
        "total_investments_amount": 2000.00,
        "risk_score": 0.75,
    }

    # Test portfolio calculation
    customer = Customer(customer_id=customer_id, first_name="Test", last_name="User")
    portfolio = await customer.calculate_portfolio(db_connection)

    assert portfolio["total_balance"] == 5000.00
    assert portfolio["total_investments"] == 3
    assert portfolio["total_investments_amount"] == 2000.00
    assert portfolio["risk_score"] == 0.75
