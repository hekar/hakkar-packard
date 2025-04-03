from sqlalchemy import text
from sqlalchemy.orm import Session


def create_views(session: Session):
    """Create database views."""
    session.execute(
        text(
            """
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
    )
    session.commit()
