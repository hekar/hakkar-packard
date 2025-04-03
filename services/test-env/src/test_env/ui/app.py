import streamlit as st
import plotly.express as px
import pandas as pd

from test_env.db.operations import (
    get_databases,
    create_database,
    drop_database,
    get_table_stats,
    get_views,
    get_indexes,
    create_schema,
    populate_database,
    run_benchmark_queries,
    get_customer_portfolio,
    get_transaction_analytics,
    get_schema_info,
    get_database_stats,
    get_index_usage_stats,
)

# Configure page
st.set_page_config(
    page_title="Database Manager",
    page_icon="🗃️",
    layout="wide",
)

# Initialize session state
if "selected_db" not in st.session_state:
    st.session_state.selected_db = None
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

# Sidebar - Database Selection
st.sidebar.title("Database Manager")

# Database Selection
st.sidebar.subheader("Select Database")
databases = get_databases()
if databases:
    selected_db = st.sidebar.selectbox(
        "Available Databases",
        options=databases,
        index=databases.index(st.session_state.selected_db)
        if st.session_state.selected_db in databases
        else 0,
        key="db_selector",
    )
    if selected_db != st.session_state.selected_db:
        st.session_state.selected_db = selected_db
        st.session_state.selected_table = None
        st.rerun()
else:
    st.sidebar.info("No databases found")

# Main Content
if st.session_state.selected_db:
    db_name = st.session_state.selected_db
    st.title(f"Database: {db_name}")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Manage Databases",
            "Definitions",
            "Statistics",
            "Populate",
            "Benchmark",
            "Analytics",
        ]
    )

    # Tab 1: Manage Databases
    with tab1:
        st.subheader("Database Management")

        # Database Creation Form
        with st.form("create_db"):
            new_db_name = st.text_input("Database Name")
            if st.form_submit_button("Create"):
                if new_db_name:
                    try:
                        create_database(new_db_name)
                        st.success(f"Database '{new_db_name}' created!")
                    except Exception as e:
                        st.error(f"Failed to create database: {e}")
                else:
                    st.warning("Please enter a database name")

        # Database Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Schema", use_container_width=True):
                try:
                    create_schema(db_name)
                    st.success("Schema created successfully!")
                except Exception as e:
                    st.error(f"Failed to create schema: {e}")

        with col2:
            if st.button("Drop Database", type="primary", use_container_width=True):
                try:
                    drop_database(db_name)
                    st.session_state.selected_db = None
                    st.session_state.selected_table = None
                    st.success(f"Database '{db_name}' dropped!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to drop database: {e}")

    # Tab 2: Definitions
    with tab2:
        st.subheader("Database Definitions")

        # Schema Information
        with st.expander("Schema Information", expanded=True):
            try:
                schema_info = get_schema_info(db_name)
                st.dataframe(schema_info)
            except Exception as e:
                st.error(f"Failed to get schema information: {e}")

        # Views
        with st.expander("Views", expanded=True):
            try:
                views_df = get_views(db_name)
                st.dataframe(views_df)
            except Exception as e:
                st.error(f"Failed to get views: {e}")

        # Indexes
        with st.expander("Indexes", expanded=True):
            try:
                indexes_df = get_indexes(db_name)
                st.dataframe(indexes_df)
            except Exception as e:
                st.error(f"Failed to get indexes: {e}")

    # Tab 3: Statistics
    with tab3:
        st.subheader("Database Statistics")

        try:
            # Basic Database Stats
            stats = get_database_stats(db_name)

            # Display basic info
            st.write("Basic Information")
            basic_info = pd.DataFrame([stats["basic_info"]])
            st.dataframe(basic_info)

            # Display table stats
            st.write("Table Statistics")
            table_stats = pd.DataFrame([stats["table_stats"]])
            st.dataframe(table_stats)

            # Display index stats
            st.write("Index Statistics")
            index_stats = pd.DataFrame([stats["index_stats"]])
            st.dataframe(index_stats)

            # Display transaction stats
            st.write("Transaction Statistics")
            transaction_stats = pd.DataFrame([stats["transaction_stats"]])
            st.dataframe(transaction_stats)

            # Table Statistics with Chart
            st.write("Table Sizes")
            tables_df = get_table_stats(db_name)
            fig = px.bar(
                tables_df,
                x="table_name",
                y="size_mb",
                title="Table Sizes",
                labels={"table_name": "Table", "size_mb": "Size (MB)"},
            )
            st.plotly_chart(fig, use_container_width=True)

            # Index Usage Statistics
            st.write("Index Usage")
            index_usage = get_index_usage_stats(db_name)
            st.dataframe(index_usage)

        except Exception as e:
            st.error(f"Failed to get database statistics: {e}")

    # Tab 4: Populate
    with tab4:
        st.subheader("Populate Database")

        with st.form("populate_data"):
            size_mb = st.number_input("Target Size (MB)", min_value=1, value=100)
            if st.form_submit_button("Populate Data"):
                try:
                    with st.spinner("Populating database..."):
                        populate_database(db_name, size_mb)
                    st.success(f"Database populated with {size_mb}MB of data!")
                except Exception as e:
                    st.error(f"Failed to populate data: {e}")

    # Tab 5: Benchmark
    with tab5:
        st.subheader("Run Benchmark")

        if st.button("Run Benchmark"):
            try:
                with st.spinner("Running benchmark queries..."):
                    benchmark_results = run_benchmark_queries(db_name)
                st.success("Benchmark completed successfully!")

                # Display benchmark results
                st.write("Portfolio Analysis")
                portfolio_df = pd.DataFrame(benchmark_results["portfolio_analysis"])
                st.dataframe(portfolio_df)

                st.write("Transaction Patterns")
                transaction_df = pd.DataFrame(benchmark_results["transaction_patterns"])
                st.dataframe(transaction_df)

                st.write("Investment Distribution")
                investment_df = pd.DataFrame(
                    benchmark_results["investment_distribution"]
                )
                st.dataframe(investment_df)

            except Exception as e:
                st.error(f"Failed to run benchmark: {e}")

    # Tab 6: Analytics
    with tab6:
        st.subheader("Database Analytics")

        # Customer Portfolio Section
        st.write("Customer Portfolio")
        customer_id = st.text_input("Enter Customer ID")
        if customer_id:
            try:
                portfolio = get_customer_portfolio(None, customer_id)
                if portfolio:
                    st.json(portfolio)
                else:
                    st.info("No portfolio found for this customer")
            except Exception as e:
                st.error(f"Failed to get customer portfolio: {e}")

        # Transaction Analytics Section
        st.write("Transaction Analytics")
        if st.button("View Transaction Analytics"):
            try:
                analytics = get_transaction_analytics(None)
                analytics_df = pd.DataFrame(analytics)
                st.dataframe(analytics_df)
            except Exception as e:
                st.error(f"Failed to get transaction analytics: {e}")

else:
    st.info("Select a database from the sidebar or create a new one.")
