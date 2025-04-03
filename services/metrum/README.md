# Metrum Query System

Metrum is a PostgreSQL monitoring and analysis tool. This repository contains the Metrum query system, which provides functionality for analyzing and caching SQL queries.

## Features

- Parse and analyze SQL queries (SELECT, UPDATE, DELETE, MERGE)
- Extract query metadata (tables, views, WHERE clause AST)
- Cache queries in SQLite for tracking and analysis
- Track whether queries have been sent to the server

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/metrum.git
cd metrum

# Install dependencies
pip install -r requirements.txt
```

## Usage

### MetrumQuery

The `MetrumQuery` class provides functionality for parsing and analyzing SQL queries:

```python
from metrum.queries import MetrumQuery

# Create a MetrumQuery instance from a query string
query = MetrumQuery.from_query("SELECT * FROM users WHERE id = 1")

# Access query metadata
print(f"Query type: {query.query_type}")
print(f"Query hash: {query.query_hash}")
print(f"Tables: {query.tables}")
print(f"Views: {query.views}")
print(f"WHERE clause AST: {query.where_clause_ast}")
```

### MetrumQueryCache and MetrumQueryCacheDb

The `MetrumQueryCache` and `MetrumQueryCacheDb` classes provide functionality for caching queries in SQLite:

```python
from metrum.queries import MetrumQuery
from metrum.db import MetrumQueryCacheDb

# Create the database tables
MetrumQueryCacheDb.create_tables()

# Create a MetrumQuery instance
query = MetrumQuery.from_query("SELECT * FROM users WHERE id = 1")

# Add the query to the cache
cache_entry = MetrumQueryCacheDb.add_query(query)

# Retrieve the query from the cache
retrieved = MetrumQueryCacheDb.get_query_by_hash(query.query_hash)

# Update the sent_to_server flag
MetrumQueryCacheDb.update_sent_to_server(query.query_hash, True)

# Get all queries
all_queries = MetrumQueryCacheDb.get_all_queries()

# Get queries by type
select_queries = MetrumQueryCacheDb.get_queries_by_type(QueryType.SELECT)
```

## Example

See the `examples/query_example.py` file for a complete example of how to use the Metrum query system.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
