from typing import Dict
import pandas as pd
from sqlalchemy import text
from .connection import get_connection
from test_env.common.logging_config import get_logger

logger = get_logger(__name__)


def get_database_stats(name: str) -> Dict:
    """Get comprehensive database statistics."""
    logger.info("starting_database_stats_collection", database_name=name)
    try:
        with get_connection(name) as conn:
            stats = {}

            # Basic database info
            logger.debug("fetching_basic_database_info")
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
            basic_info = result.fetchone()
            logger.debug("basic_database_info_result", result=basic_info)
            stats["basic_info"] = dict(zip(result.keys(), basic_info))
            logger.debug("basic_info_stats", stats=stats["basic_info"])

            # Table statistics
            logger.debug("fetching_table_statistics")
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
            table_stats = result.fetchone()
            logger.debug("table_statistics_result", result=table_stats)
            stats["table_stats"] = dict(zip(result.keys(), table_stats))
            logger.debug("table_stats", stats=stats["table_stats"])

            # Index statistics
            logger.debug("fetching_index_statistics")
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
            index_stats = result.fetchone()
            logger.debug("index_statistics_result", result=index_stats)
            stats["index_stats"] = dict(zip(result.keys(), index_stats))
            logger.debug("index_stats", stats=stats["index_stats"])

            # Individual table statistics
            logger.debug("fetching_individual_table_statistics")
            result = conn.execute(
                text(
                    """
                SELECT 
                    schemaname || '.' || relname as table_name,
                    seq_scan,
                    last_seq_scan,
                    seq_tup_read,
                    idx_scan,
                    last_idx_scan,
                    idx_tup_fetch,
                    n_tup_ins,
                    n_tup_upd,
                    n_tup_del,
                    n_tup_hot_upd,
                    n_tup_newpage_upd,
                    n_live_tup,
                    n_dead_tup,
                    n_mod_since_analyze,
                    n_ins_since_vacuum,
                    last_vacuum,
                    last_autovacuum,
                    last_analyze,
                    last_autoanalyze,
                    vacuum_count,
                    autovacuum_count,
                    analyze_count,
                    autoanalyze_count
                FROM pg_stat_user_tables
                ORDER BY n_live_tup DESC
                """
                )
            )
            individual_table_stats = result.fetchall()
            logger.debug("individual_table_statistics_result", result=individual_table_stats)
            stats["individual_table_stats"] = [
                dict(zip(result.keys(), row)) for row in individual_table_stats
            ]
            logger.debug("individual_table_stats", stats=stats["individual_table_stats"])

            # Transaction statistics
            logger.debug("fetching_transaction_statistics")
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
            row = result.fetchone()
            logger.debug("transaction_statistics_raw_result", result=row)
            logger.debug("transaction_statistics_columns", columns=result.keys())
            if row:
                try:
                    stats["transaction_stats"] = dict(zip(result.keys(), row))
                    logger.debug("transaction_stats", stats=stats["transaction_stats"])
                except Exception as e:
                    logger.error("error_creating_transaction_stats",
                               error=str(e),
                               row_data=row,
                               column_names=result.keys())
                    raise
            else:
                logger.warning("no_transaction_statistics_found")
                stats["transaction_stats"] = {}

            logger.info("database_statistics_collection_complete")
            return stats
    except Exception as e:
        logger.error("error_collecting_database_statistics",
                    error=e,
                    database_name=name,
                    exc_info=True)
        raise


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
