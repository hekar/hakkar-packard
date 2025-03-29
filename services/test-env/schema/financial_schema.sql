-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create tables
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

-- Create views
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