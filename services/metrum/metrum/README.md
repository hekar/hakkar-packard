# Metrum - PostgreSQL Log Monitor

Metrum is a tool for monitoring PostgreSQL logs and analyzing query performance.

## Features

- Monitors PostgreSQL log files in real-time
- Extracts query text, execution plans, and duration information
- Categorizes queries based on configurable patterns
- Stores log events in a database for analysis
- Sends events to an HTTP endpoint for further processing

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```
   python -m metrum.db.migrations.run_migrations
   ```

## Configuration

### Database

Configure the database connection in `metrum/settings.py`:

```python
database_url = "postgresql://username:password@localhost:5432/metrum"
```

### Patterns

Edit the patterns file at `metrum/config/patterns.json` to define query patterns to match:

```json
{
  "slow_query": {
    "query_pattern": "SELECT.*FROM.*WHERE.*",
    "description": "Slow SELECT queries"
  },
  "insert_query": {
    "query_pattern": "INSERT INTO.*",
    "description": "INSERT queries"
  }
}
```

## Usage

Run the log monitor:

```
python -m metrum.scripts.run_log_monitor --log-file /path/to/postgresql.log --patterns metrum/config/patterns.json --http-endpoint http://localhost:8000/api/events
```

### Command-line Arguments

- `--log-file`: Path to the PostgreSQL log file
- `--patterns`: Path to the patterns JSON file
- `--http-endpoint`: HTTP endpoint to send events to
- `--poll-interval`: Poll interval in seconds (default: 1.0)

## Database Schema

### log_events Table

- `id`: Primary key
- `timestamp`: Timestamp of the log event
- `query_text`: The SQL query text
- `explain_text`: The execution plan
- `duration_ms`: Query duration in milliseconds
- `pattern_name`: Name of the matched pattern
- `status`: Event status (pending, sent, failed)
- `created_at`: When the event was created
- `updated_at`: When the event was last updated

## License

MIT 