import pandas as pd
from sqlalchemy import text, inspect
from typing import List, Dict, Any
from .connection import get_connection, get_db_session


def get_schema_info(db_name: str, tablename: str | None = None) -> pd.DataFrame:
    """Get detailed schema information including tables, columns, and their types.

    Args:
        db_name: Database name
        tablename: Optional table name to filter by
    """
    with get_db_session(db_name) as session:
        inspector = inspect(session.connection())

        # Get all tables in public schema or specific table if provided
        tables = inspector.get_table_names()

        # Collect schema information for each table
        schema_info: List[Dict[str, Any]] = []
        for table in tables:
            columns = inspector.get_columns(table)
            for col in columns:
                schema_info.append(
                    {
                        "table_name": table,
                        "column_name": col["name"],
                        "data_type": str(col["type"]),
                        "character_maximum_length": getattr(
                            col["type"], "length", None
                        ),
                        "is_nullable": "YES" if col.get("nullable", True) else "NO",
                        "column_default": col.get("default", None),
                    }
                )

        return pd.DataFrame(schema_info)


def get_views(name: str, viewname: str | None = None) -> pd.DataFrame:
    """Get database views with their definitions.

    Args:
        name: Database name
        viewname: Optional view name to filter by
    """
    with get_connection(name) as conn:
        query = text(
            """
        SELECT 
            schemaname || '.' || viewname as view_name,
            definition as view | None = None           pg_size_pretty(pg_relation_size(schemaname || '.' || viewname)) as view_size
        FROM pg_views
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        """
            + (" AND viewname = :viewname" if viewname else "")
            + """
        ORDER BY view_name;
        """
        )
        params = {"viewname": viewname} if viewname else {}
        return pd.read_sql(query, conn, params=params)


def get_indexes(db_name: str, tablename: str | None = None) -> pd.DataFrame:
    """Get database indexes with detailed information.

    Args:
        db_name: Database name
        tablename: Optional table name to filter by
    """
    with get_connection(db_name) as conn:
        query = text(
            """
        SELECT 
            schemaname || '.' || tablename as table_name,
            indexname as index_name,
            indexdef as index_ddl,
            pg_size_pretty(pg_relation_size(schemaname || '.' || indexname)) as index_size,
            CASE WHEN indexdef LIKE '%UNIQUE%' THEN true ELSE false END as is_unique
        FROM pg_indexes
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        """
            + (" AND tablename = :name" if tablename else "")
            + """
        ORDER BY tablename, indexname;
        """
        )
        params = {"name": tablename} if tablename else {}
        return pd.read_sql(query, conn, params=params)
