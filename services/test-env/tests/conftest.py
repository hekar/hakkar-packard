import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from testcontainers.postgres import PostgresContainer
from test_env.db import create_schema, populate_database
import os
import asyncpg


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container and set environment variables."""
    container = PostgresContainer(
        image="postgres:17", username="postgres", password="postgres", dbname="postgres"
    ).with_exposed_ports(5432)
    container.start()

    # Set environment variables for database connection
    os.environ["TEST_ENV_DB_HOST"] = container.get_container_host_ip()
    os.environ["TEST_ENV_DB_PORT"] = str(container.get_exposed_port(5432))
    os.environ["TEST_ENV_DB_USER"] = "postgres"
    os.environ["TEST_ENV_DB_PASSWORD"] = "postgres"
    os.environ["TEST_ENV_DB_NAME"] = "postgres"

    # Print connection info for debugging
    print(f"Container host: {os.environ['TEST_ENV_DB_HOST']}")
    print(f"Container port: {os.environ['TEST_ENV_DB_PORT']}")

    yield container

    container.stop()


@pytest.fixture(scope="session")
def patched_db_connection(postgres_container):
    """Patch get_db_connection to use the container's connection details."""

    async def container_db_connection():
        return await asyncpg.connect(
            host=postgres_container.get_container_host_ip(),
            port=postgres_container.get_exposed_port(5432),
            user="postgres",
            password="postgres",
            database="postgres",
        )

    with patch("test_env.db.get_db_connection", container_db_connection):
        yield container_db_connection


@pytest.fixture
async def db_connection(request, patched_db_connection):
    """Provide a database connection for tests."""
    if request.node.get_closest_marker("uses_testcontainer"):
        conn = await patched_db_connection()

        await create_schema()

        yield conn

        await conn.execute(
            """
            TRUNCATE TABLE investments CASCADE;
            TRUNCATE TABLE transactions CASCADE;
            TRUNCATE TABLE accounts CASCADE;
            TRUNCATE TABLE customers CASCADE;
        """
        )
        await populate_database(target_size_mb=2)
        await conn.close()
    else:
        # Use mock connection for other tests
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_conn.fetchval = AsyncMock()
        mock_conn.fetchrow = AsyncMock()
        mock_conn.fetch = AsyncMock()
        yield mock_conn
