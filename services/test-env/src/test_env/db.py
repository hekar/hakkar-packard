import logging
import asyncpg
from pathlib import Path
from .config import settings

logger = logging.getLogger(__name__)


def read_sql_file(file_path: str) -> str:
    """Read SQL from a file."""
    path = Path(file_path)
    if not path.is_absolute():
        # If relative path, make it relative to the project root
        project_root = Path(__file__).parent.parent.parent
        path = project_root / path

    with open(path, "r") as f:
        contents = f.read()
        logging.debug("logger")
        return contents


async def get_db_connection():
    """Get a database connection."""
    return await asyncpg.connect(
        host=settings.db.host,
        port=settings.db.port,
        user=settings.db.user,
        password=settings.db.password,
        database=settings.db.database,
    )


async def create_schema():
    """Create database schema."""
    conn = await get_db_connection()
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id UUID PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS accounts (
                account_id UUID PRIMARY KEY,
                customer_id UUID REFERENCES customers(customer_id),
                balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id UUID PRIMARY KEY,
                account_id UUID REFERENCES accounts(account_id),
                transaction_type TEXT NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS investments (
                investment_id UUID PRIMARY KEY,
                account_id UUID REFERENCES accounts(account_id),
                amount DECIMAL(15,2) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE OR REPLACE VIEW customer_portfolio AS
            SELECT 
                c.customer_id,
                SUM(a.balance) as total_balance,
                SUM(i.amount) as total_investments
            FROM customers c
            LEFT JOIN accounts a ON a.customer_id = c.customer_id
            LEFT JOIN investments i ON i.account_id = a.account_id
            GROUP BY c.customer_id;

            CREATE OR REPLACE VIEW transaction_analytics AS
            SELECT 
                transaction_type,
                COUNT(*) as count,
                SUM(amount) as total_amount
            FROM transactions
            GROUP BY transaction_type;
        """
        )
    finally:
        await conn.close()


async def populate_database(target_size_mb: int = 100):
    """Populate database with test data."""
    conn = await get_db_connection()
    try:
        await conn.execute(
            """
            INSERT INTO customers (customer_id, first_name, last_name)
            SELECT 
                gen_random_uuid(),
                'Customer' || i,
                'Last' || i
            FROM generate_series(1, 1000) i;

            INSERT INTO accounts (account_id, customer_id, balance)
            SELECT 
                gen_random_uuid(),
                customer_id,
                random() * 10000
            FROM customers
            CROSS JOIN generate_series(1, 3);

            INSERT INTO transactions (transaction_id, account_id, transaction_type, amount)
            SELECT 
                gen_random_uuid(),
                account_id,
                CASE WHEN random() > 0.5 THEN 'deposit' ELSE 'withdrawal' END,
                random() * 1000
            FROM accounts
            CROSS JOIN generate_series(1, 5);

            INSERT INTO investments (investment_id, account_id, amount)
            SELECT 
                gen_random_uuid(),
                account_id,
                random() * 5000
            FROM accounts
            WHERE random() > 0.7;
        """
        )
    finally:
        await conn.close()


async def run_benchmark_queries():
    """Run benchmark queries."""
    conn = await get_db_connection()
    try:
        await conn.execute(
            """
            -- Query 1: Customer portfolio analysis
            SELECT c.customer_id, 
                   COUNT(DISTINCT a.account_id) as num_accounts,
                   SUM(a.balance) as total_balance,
                   COUNT(DISTINCT i.investment_id) as num_investments,
                   SUM(i.amount) as total_investments
            FROM customers c
            LEFT JOIN accounts a ON a.customer_id = c.customer_id
            LEFT JOIN investments i ON i.account_id = a.account_id
            GROUP BY c.customer_id;

            -- Query 2: Transaction patterns
            SELECT DATE_TRUNC('hour', created_at) as hour,
                   transaction_type,
                   COUNT(*) as num_transactions,
                   SUM(amount) as total_amount
            FROM transactions
            GROUP BY hour, transaction_type
            ORDER BY hour;

            -- Query 3: Investment distribution
            SELECT a.account_id,
                   a.balance as account_balance,
                   COUNT(i.investment_id) as num_investments,
                   SUM(i.amount) as total_invested,
                   SUM(i.amount) / a.balance as investment_ratio
            FROM accounts a
            LEFT JOIN investments i ON i.account_id = a.account_id
            GROUP BY a.account_id, a.balance
            HAVING a.balance > 0;
        """
        )
    finally:
        await conn.close()


async def get_customer_portfolio(customer_id: str):
    """Get customer portfolio information."""
    conn = await get_db_connection()
    try:
        return await conn.fetchrow(
            """
            SELECT * FROM customer_portfolio WHERE customer_id = $1
        """,
            customer_id,
        )
    finally:
        await conn.close()


async def get_transaction_analytics():
    """Get transaction analytics information."""
    conn = await get_db_connection()
    try:
        return await conn.fetch(
            """
            SELECT * FROM transaction_analytics
        """
        )
    finally:
        await conn.close()
