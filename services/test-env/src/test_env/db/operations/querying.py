from typing import Optional, List, Tuple
import pandas as pd
from sqlalchemy import text
from .connection import get_connection


def get_column_info(conn, table_name: str) -> List[Tuple[str, str]]:
    """Get column information for a table."""
    result = conn.execute(
        text(
            """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = :table_name
    """
        ),
        {"table_name": table_name.split(".")[-1]},
    )
    return [(row[0], row[1]) for row in result]


def build_search_query(
    table_name: str, columns: List[Tuple[str, str]], search: str
) -> Tuple[str, dict]:
    """Build search query with parameters."""
    where_clauses = []
    params = {}
    param_count = 0

    for col, dtype in columns:
        if dtype in ("character varying", "text"):
            param_name = f"p{param_count}"
            where_clauses.append(f"{col}::text ILIKE :{param_name}")
            params[param_name] = f"%{search}%"
            param_count += 1
        elif dtype in ("integer", "bigint", "numeric"):
            try:
                float(search)
                param_name = f"p{param_count}"
                where_clauses.append(f"{col}::text ILIKE :{param_name}")
                params[param_name] = f"%{search}%"
                param_count += 1
            except ValueError:
                continue

    query = f"SELECT * FROM {table_name}"
    if where_clauses:
        query += " WHERE " + " OR ".join(where_clauses)

    return query, params


def get_table_data(
    name: str, table_name: str, search: Optional[str] = None, offset: int = 0
) -> pd.DataFrame:
    """Get table data with optional search filter."""
    with get_connection(name) as conn:
        if search:
            columns = get_column_info(conn, table_name)
            query, params = build_search_query(table_name, columns, search)
        else:
            query = f"SELECT * FROM {table_name}"
            params = {}

        query += f" LIMIT 50 OFFSET {offset}"
        return pd.read_sql(text(query), conn, params=params)


def get_table_row_count(
    name: str, table_name: str, search: Optional[str] = None
) -> int:
    """Get total row count for pagination."""
    with get_connection(name) as conn:
        if search:
            columns = get_column_info(conn, table_name)
            base_query, params = build_search_query(table_name, columns, search)
            query = f"SELECT COUNT(*) FROM ({base_query}) as subq"
        else:
            query = f"SELECT COUNT(*) FROM {table_name}"
            params = {}

        result = conn.execute(text(query), params)
        return result.scalar()
