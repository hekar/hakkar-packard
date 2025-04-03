from sqlalchemy import text
from sqlalchemy.orm import Session
from ..connection import get_db_session


def run_benchmark_queries(db_name: str):
    """Run benchmark queries."""
    with get_db_session(db_name) as session:
        # Query 1: Customer portfolio analysis
        result = session.execute(
            text(
                """
            SELECT c.customer_id, 
                   COUNT(DISTINCT a.account_id) as num_accounts,
                   SUM(a.balance) as total_balance,
                   COUNT(DISTINCT i.investment_id) as num_investments,
                   SUM(i.amount) as total_investments
            FROM customers c
            LEFT JOIN accounts a ON a.customer_id = c.customer_id
            LEFT JOIN investments i ON i.account_id = a.account_id
            GROUP BY c.customer_id;
            """
            )
        )
        portfolio_analysis = result.fetchall()

        # Query 2: Transaction patterns
        result = session.execute(
            text(
                """
            SELECT DATE_TRUNC('hour', created_at) as hour,
                   transaction_type,
                   COUNT(*) as num_transactions,
                   SUM(amount) as total_amount
            FROM transactions
            GROUP BY hour, transaction_type
            ORDER BY hour;
            """
            )
        )
        transaction_patterns = result.fetchall()

        # Query 3: Investment distribution
        result = session.execute(
            text(
                """
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
        )
        investment_distribution = result.fetchall()

        return {
            "portfolio_analysis": portfolio_analysis,
            "transaction_patterns": transaction_patterns,
            "investment_distribution": investment_distribution,
        }


def get_customer_portfolio(session: Session, customer_id: str = None):
    """Get customer portfolio information."""
    result = session.execute(
        text("SELECT * FROM customer_portfolio WHERE customer_id = :customer_id"),
        {"customer_id": customer_id},
    )
    return result.fetchone()


def get_transaction_analytics(session: Session):
    """Get transaction analytics information."""
    result = session.execute(text("SELECT * FROM transaction_analytics"))
    return result.fetchall()
