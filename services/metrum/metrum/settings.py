import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database settings
database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/metrum")

# Log monitor settings
default_poll_interval = float(os.getenv("LOG_MONITOR_POLL_INTERVAL", "1.0"))
default_http_endpoint = os.getenv("LOG_MONITOR_HTTP_ENDPOINT", "http://localhost:8000/api/events")
default_patterns_file = os.getenv("LOG_MONITOR_PATTERNS_FILE", "metrum/config/patterns.json") 