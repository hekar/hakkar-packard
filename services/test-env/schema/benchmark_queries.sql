-- Complex join with aggregation
-- Query 1: Customer transaction summary for last 30 days
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

-- Complex view with window functions
-- Query 2: Customer rankings by balance
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

-- Complex subquery with multiple joins
-- Query 3: Active accounts with recent activity and investments
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