import subprocess
import os

import pandas as pd
import plotly.express as px
import psycopg
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Test Database Manager",
    page_icon="🗃️",
    layout="wide",
)


def get_connection(dbname: str = "postgres") -> psycopg.Connection:
    """Get database connection."""
    return psycopg.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="postgres",
        dbname=dbname,
        autocommit=True,
    )


def get_databases() -> list[str]:
    """Get list of databases."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT datname 
                FROM pg_database 
                WHERE datistemplate = false 
                AND datname != 'postgres'
                ORDER BY datname;
            """
            )
            return [row[0] for row in cur.fetchall()]


def create_database(name: str):
    """Create a new database."""
    with get_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {name};")


def drop_database(name: str):
    """Drop a database."""
    with get_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            # Terminate all connections to the database
            cur.execute(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{name}'
                AND pid <> pg_backend_pid();
            """
            )
            cur.execute(f"DROP DATABASE IF EXISTS {name};")


def get_database_size(name: str) -> float:
    """Get database size in MB."""
    with get_connection(name) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT pg_database_size(current_database()) / 1024.0 / 1024.0;"
            )
            return cur.fetchone()[0]


def get_table_stats(name: str) -> pd.DataFrame:
    """Get table statistics."""
    with get_connection(name) as conn:
        query = """
        SELECT 
            schemaname || '.' || tablename as table_name,
            n_live_tup as row_count,
            pg_total_relation_size(schemaname || '.' || tablename) / 1024.0 / 1024.0 as size_mb
        FROM pg_stat_user_tables
        ORDER BY n_live_tup DESC;
        """
        return pd.read_sql(query, conn)


def run_migrations(name: str):
    """Run database migrations."""
    try:
        subprocess.run(
            ["poetry", "run", "python", "src/test_env", "migrate-db"],
            check=True,
            env={**os.environ, "TEST_ENV_DB_DATABASE": name},
        )
        st.success("Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"Migration failed: {e}")


def populate_test_data(name: str):
    """Populate database with test data."""
    try:
        subprocess.run(
            ["poetry", "run", "python", "src/test_env", "populate-db"],
            check=True,
            env={**os.environ, "TEST_ENV_DB_DATABASE": name},
        )
        st.success("Test data populated successfully!")
    except subprocess.CalledProcessError as e:
        st.error(f"Data population failed: {e}")


# Sidebar
st.sidebar.title("Test Database Manager")

# Database creation
with st.sidebar.form("create_db"):
    st.write("Create New Database")
    new_db_name = st.text_input("Database Name")
    create_submitted = st.form_submit_button("Create")

    if create_submitted and new_db_name:
        try:
            create_database(new_db_name)
            st.success(f"Database '{new_db_name}' created!")
        except Exception as e:
            st.error(f"Failed to create database: {e}")

# Database selection
databases = get_databases()
selected_db = st.sidebar.selectbox("Select Database", databases)

if selected_db:
    # Database actions
    st.sidebar.subheader("Actions")
    col1, col2, col3 = st.sidebar.columns(3)

    if col1.button("Run Migrations"):
        run_migrations(selected_db)

    if col2.button("Populate Data"):
        populate_test_data(selected_db)

    if col3.button("Drop Database"):
        if st.sidebar.checkbox("Confirm drop?"):
            try:
                drop_database(selected_db)
                st.success(f"Database '{selected_db}' dropped!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to drop database: {e}")

    # Main content
    st.title(f"Database: {selected_db}")

    # Database size
    size_mb = get_database_size(selected_db)
    st.metric("Database Size", f"{size_mb:.2f} MB")

    # Table statistics
    st.subheader("Table Statistics")
    try:
        df = get_table_stats(selected_db)

        # Table size chart
        fig_size = px.bar(
            df,
            x="table_name",
            y="size_mb",
            title="Table Sizes",
            labels={"table_name": "Table", "size_mb": "Size (MB)"},
        )
        st.plotly_chart(fig_size, use_container_width=True)

        # Row count chart
        fig_rows = px.bar(
            df,
            x="table_name",
            y="row_count",
            title="Row Counts",
            labels={"table_name": "Table", "row_count": "Number of Rows"},
        )
        st.plotly_chart(fig_rows, use_container_width=True)

        # Detailed table
        st.dataframe(
            df.style.format({"size_mb": "{:.2f}", "row_count": "{:,.0f}"}),
            hide_index=True,
        )
    except Exception as e:
        st.error(f"Failed to get table statistics: {e}")
else:
    st.info("No test databases found. Create one using the form in the sidebar.")
