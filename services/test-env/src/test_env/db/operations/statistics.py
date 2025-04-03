from typing import Dict
import pandas as pd
from sqlalchemy import text
from .connection import get_connection


def get_database_stats(name: str) -> Dict:
    """Get comprehensive database statistics."""
    with get_connection(name) as conn:
        stats = {}

        # Basic database info
        result = conn.execute(
            text(
                """
            SELECT 
                current_database() as database_name,
                version() as postgres_version,
                pg_size_pretty(pg_database_size(current_database())) as total_size,
                pg_database_size(current_database()) / 1024.0 / 1024.0 as size_mb
        """
            )
        )
        stats["basic_info"] = dict(result.fetchone())

        # Table statistics
        result = conn.execute(
            text(
                """
            SELECT 
                COUNT(*) as total_tables,
                SUM(n_live_tup) as total_rows,
                SUM(pg_total_relation_size(schemaname || '.' || relname)) / 1024.0 / 1024.0 as total_size_mb
            FROM pg_stat_user_tables
        """
            )
        )
        stats["table_stats"] = dict(result.fetchone())

        # Index statistics
        result = conn.execute(
            text(
                """
            SELECT 
                COUNT(*) as total_indexes,
                SUM(pg_relation_size(schemaname || '.' || indexrelname)) / 1024.0 / 1024.0 as total_size_mb
            FROM pg_stat_user_indexes
        """
            )
        )
        stats["index_stats"] = dict(result.fetchone())

        # Transaction statistics
        result = conn.execute(
            text(
                """
            SELECT 
                xact_commit as transactions_committed,
                xact_rollback as transactions_rolled_back,
                blks_read as blocks_read,
                blks_hit as blocks_hit,
                tup_returned as rows_returned,
                tup_fetched as rows_fetched,
                tup_inserted as rows_inserted,
                tup_updated as rows_updated,
                tup_deleted as rows_deleted
            FROM pg_stat_database
            WHERE datname = current_database()
        """
            )
        )
        stats["transaction_stats"] = dict(result.fetchone())

        return stats


def get_table_stats(name: str) -> pd.DataFrame:
    """Get detailed table statistics."""
    with get_connection(name) as conn:
        query = text(
            """
        SELECT 
            schemaname || '.' || relname as table_name,
            n_live_tup as row_count,
            n_dead_tup as dead_tuples,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze,
            pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) as total_size,
            pg_size_pretty(pg_table_size(schemaname || '.' || relname)) as table_size,
            pg_size_pretty(pg_indexes_size(schemaname || '.' || relname)) as index_size,
            pg_total_relation_size(schemaname || '.' || relname) / 1024.0 / 1024.0 as size_mb
        FROM pg_stat_user_tables
        ORDER BY pg_total_relation_size(schemaname || '.' || relname) DESC;
        """
        )
        return pd.read_sql(query, conn)


def get_index_usage_stats(name: str) -> pd.DataFrame:
    """Get index usage statistics."""
    with get_connection(name) as conn:
        query = text(
            """
        SELECT 
            schemaname || '.' || relname as table_name,
            indexrelname as index_name,
            idx_scan as index_scans,
            idx_tup_read as tuples_read,
            idx_tup_fetch as tuples_fetched,
            pg_size_pretty(pg_relation_size(schemaname || '.' || indexrelname)) as index_size
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC;
        """
        )
        return pd.read_sql(query, conn)
