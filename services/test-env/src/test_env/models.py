import uuid
from typing import Dict, Any


class Customer:
    def __init__(self, customer_id: str, first_name: str, last_name: str):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    async def create(cls, db, first_name: str, last_name: str) -> "Customer":
        customer_id = str(uuid.uuid4())
        await db.execute(
            """
            INSERT INTO customers (customer_id, first_name, last_name)
            VALUES ($1, $2, $3)
            """,
            customer_id,
            first_name,
            last_name,
        )
        return cls(customer_id=customer_id, first_name=first_name, last_name=last_name)

    async def calculate_portfolio(self, db) -> Dict[str, Any]:
        result = await db.fetchrow(
            """
            SELECT 
                SUM(a.balance) as total_balance,
                COUNT(i.*) as total_investments,
                SUM(i.amount) as total_investments_amount,
                COALESCE(AVG(CASE WHEN i.amount > 0 THEN i.amount::float / a.balance ELSE 0 END), 0) as risk_score
            FROM customers c
            LEFT JOIN accounts a ON c.customer_id = a.customer_id
            LEFT JOIN investments i ON a.account_id = i.account_id
            WHERE c.customer_id = $1
            GROUP BY c.customer_id
            """,
            self.customer_id,
        )
        return (
            dict(result)
            if result
            else {
                "total_balance": 0.0,
                "total_investments": 0,
                "total_investments_amount": 0.0,
                "risk_score": 0.0,
            }
        )


class Account:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance

    async def update_balance(self, db, amount: float) -> None:
        """Update account balance with the given amount (positive for deposit, negative for withdrawal)."""
        await db.execute(
            """
            UPDATE accounts 
            SET balance = balance + $2
            WHERE account_id = $1
            """,
            self.account_id,
            amount,
        )
        self.balance += amount


class Transaction:
    def __init__(
        self, transaction_id: str, account_id: str, transaction_type: str, amount: float
    ):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount

    async def validate(self, db, account: Account) -> None:
        """Validate transaction before execution."""
        if self.transaction_type == "WITHDRAWAL" and self.amount > account.balance:
            raise ValueError("Insufficient funds")


class Investment:
    def __init__(self, investment_id: str, account_id: str, amount: float):
        self.investment_id = investment_id
        self.account_id = account_id
        self.amount = amount

    async def allocate(self, db) -> None:
        """Allocate investment amount from account balance."""
        # First check if account has sufficient balance
        account_data = await db.fetchrow(
            "SELECT balance FROM accounts WHERE account_id = $1", self.account_id
        )

        if not account_data or account_data["balance"] < self.amount:
            raise ValueError("Insufficient funds for investment")

        # Create investment and update account balance
        await db.execute(
            """
            INSERT INTO investments (investment_id, account_id, amount)
            VALUES ($1, $2, $3)
            """,
            self.investment_id,
            self.account_id,
            self.amount,
        )

        await db.execute(
            """
            UPDATE accounts 
            SET balance = balance - $2
            WHERE account_id = $1
            """,
            self.account_id,
            self.amount,
        )
