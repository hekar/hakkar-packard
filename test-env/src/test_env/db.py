import asyncpg
import random
from datetime import datetime, timedelta
import uuid
import time
import asyncio

async def get_db_connection():
    """Create a database connection."""
    return await asyncpg.connect(
        user="postgres",
        password="postgres",
        database="postgres",
        host="localhost",
        port=5432
    )

async def create_schema():
    """Create the database schema with complex financial tables and views."""
    conn = await get_db_connection()
    
    # Enable pg_stat_statements extension
    await conn.execute("""
        CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    """)
    
    # Create tables
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id UUID PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(20),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS accounts (
            account_id UUID PRIMARY KEY,
            customer_id UUID REFERENCES customers(customer_id),
            account_type VARCHAR(50),
            balance DECIMAL(15,2),
            currency VARCHAR(3),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id UUID PRIMARY KEY,
            account_id UUID REFERENCES accounts(account_id),
            transaction_type VARCHAR(50),
            amount DECIMAL(15,2),
            description TEXT,
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS investments (
            investment_id UUID PRIMARY KEY,
            account_id UUID REFERENCES accounts(account_id),
            investment_type VARCHAR(50),
            amount DECIMAL(15,2),
            risk_level VARCHAR(20),
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS market_data (
            market_data_id UUID PRIMARY KEY,
            symbol VARCHAR(10),
            price DECIMAL(15,2),
            volume BIGINT,
            timestamp TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create views
    await conn.execute("""
        CREATE OR REPLACE VIEW customer_portfolio AS
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            COUNT(DISTINCT a.account_id) as total_accounts,
            SUM(a.balance) as total_balance,
            COUNT(DISTINCT i.investment_id) as total_investments,
            SUM(i.amount) as total_investments_amount
        FROM customers c
        LEFT JOIN accounts a ON c.customer_id = a.customer_id
        LEFT JOIN investments i ON a.account_id = i.account_id
        GROUP BY c.customer_id, c.first_name, c.last_name;

        CREATE OR REPLACE VIEW transaction_analytics AS
        SELECT 
            a.account_id,
            COUNT(*) as total_transactions,
            SUM(CASE WHEN t.transaction_type = 'DEPOSIT' THEN t.amount ELSE 0 END) as total_deposits,
            SUM(CASE WHEN t.transaction_type = 'WITHDRAWAL' THEN t.amount ELSE 0 END) as total_withdrawals,
            AVG(t.amount) as avg_transaction_amount
        FROM accounts a
        LEFT JOIN transactions t ON a.account_id = t.account_id
        GROUP BY a.account_id;
    """)

    await conn.close()

async def populate_database(target_size_mb):
    """Populate the database with random financial data."""
    conn = await get_db_connection()
    
    # Get current timestamp for unique suffix
    timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create a shorter unique identifier for phone numbers
    phone_suffix = str(random.randint(1000, 9999))
    
    # Calculate number of records based on target size
    # Assuming average record size of ~1KB, we'll generate more records
    num_customers = 10000  # Increased from 1000
    num_market_data = 100000  # Increased from 10000
    
    # Generate customers
    customers_data = [
        (str(uuid.uuid4()), f"First{i}", f"Last{i}", f"email{i}_{timestamp_suffix}@example.com", 
         f"+1234567890{i}_{phone_suffix}", f"Address {i}", datetime.now(), datetime.now())
        for i in range(num_customers)
    ]
    
    # Use copy_from for faster bulk insert
    await conn.copy_records_to_table(
        'customers',
        records=customers_data,
        columns=['customer_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'created_at', 'updated_at']
    )

    # Generate accounts (2-4 accounts per customer)
    accounts_data = [
        (str(uuid.uuid4()), str(customer[0]), random.choice(['SAVINGS', 'CHECKING', 'INVESTMENT']),
         random.uniform(1000, 1000000), random.choice(['USD', 'EUR', 'GBP']),
         random.choice(['ACTIVE', 'INACTIVE', 'PENDING']), datetime.now(), datetime.now())
        for customer in customers_data
        for _ in range(random.randint(2, 4))
    ]
    
    await conn.copy_records_to_table(
        'accounts',
        records=accounts_data,
        columns=['account_id', 'customer_id', 'account_type', 'balance', 'currency', 'status', 'created_at', 'updated_at']
    )

    # Generate transactions (10-30 transactions per account)
    transactions_data = [
        (str(uuid.uuid4()), str(account[0]), random.choice(['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']),
         random.uniform(10, 10000), f"Transaction {i}_{timestamp_suffix}", random.choice(['COMPLETED', 'PENDING', 'FAILED']),
         datetime.now() - timedelta(days=random.randint(0, 365)))
        for account in accounts_data
        for i in range(random.randint(10, 30))
    ]
    
    await conn.copy_records_to_table(
        'transactions',
        records=transactions_data,
        columns=['transaction_id', 'account_id', 'transaction_type', 'amount', 'description', 'status', 'created_at']
    )

    # Generate investments (1-2 investments per investment account)
    investments_data = [
        (str(uuid.uuid4()), str(account[0]), random.choice(['STOCKS', 'BONDS', 'MUTUAL_FUNDS']),
         random.uniform(1000, 50000), random.choice(['LOW', 'MEDIUM', 'HIGH']),
         datetime.now() - timedelta(days=random.randint(0, 365)),
         datetime.now() + timedelta(days=random.randint(30, 365)),
         datetime.now())
        for account in accounts_data
        if account[2] == 'INVESTMENT'
        for _ in range(random.randint(1, 2))
    ]
    
    await conn.copy_records_to_table(
        'investments',
        records=investments_data,
        columns=['investment_id', 'account_id', 'investment_type', 'amount', 'risk_level', 'start_date', 'end_date', 'created_at']
    )

    # Generate market data (more frequent updates)
    market_data_data = [
        (str(uuid.uuid4()), random.choice(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'INTC', 'ORCL']),
         random.uniform(100, 1000), random.randint(1000000, 10000000),
         datetime.now() - timedelta(minutes=random.randint(0, 1440)),
         datetime.now())
        for _ in range(num_market_data)
    ]
    
    await conn.copy_records_to_table(
        'market_data',
        records=market_data_data,
        columns=['market_data_id', 'symbol', 'price', 'volume', 'timestamp', 'created_at']
    )

    await conn.close()

async def run_benchmark_queries():
    """Run various complex queries to benchmark the database."""
    conn = await get_db_connection()
    
    queries = [
        # Complex join with aggregation
        """
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            COUNT(DISTINCT t.transaction_id) as total_transactions,
            SUM(t.amount) as total_amount,
            AVG(t.amount) as avg_amount
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        JOIN transactions t ON a.account_id = t.account_id
        WHERE t.created_at >= NOW() - INTERVAL '30 days'
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING COUNT(DISTINCT t.transaction_id) > 10
        ORDER BY total_amount DESC
        LIMIT 100;
        """,
        
        # Complex view with window functions
        """
        WITH customer_rankings AS (
            SELECT 
                customer_id,
                total_balance,
                ROW_NUMBER() OVER (ORDER BY total_balance DESC) as balance_rank,
                PERCENT_RANK() OVER (ORDER BY total_balance) as balance_percentile
            FROM customer_portfolio
        )
        SELECT *
        FROM customer_rankings
        WHERE balance_rank <= 10
        OR balance_percentile <= 0.1;
        """,
        
        # Complex subquery with multiple joins
        """
        SELECT 
            a.account_id,
            a.balance,
            (
                SELECT COUNT(*)
                FROM transactions t
                WHERE t.account_id = a.account_id
                AND t.created_at >= NOW() - INTERVAL '7 days'
            ) as recent_transactions,
            (
                SELECT SUM(amount)
                FROM investments i
                WHERE i.account_id = a.account_id
                AND i.end_date >= NOW()
            ) as active_investments
        FROM accounts a
        WHERE a.status = 'ACTIVE'
        AND a.balance > 10000;
        """
    ]
    
    results = []
    for query in queries:
        start_time = time.time()
        await conn.fetch(query)
        end_time = time.time()
        execution_time = end_time - start_time
        results.append({
            'query': query[:100] + '...',
            'execution_time': execution_time
        })
    
    await conn.close()
    return results 