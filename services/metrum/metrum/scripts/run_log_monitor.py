import asyncio
import os
import sys
import argparse
import json
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from metrum.logs.log_monitor import LogMonitor
from metrum.settings import settings

async def main():
    """Run the log monitor."""
    parser = argparse.ArgumentParser(description='Monitor PostgreSQL logs')
    parser.add_argument('--log-file', type=str, required=True, help='Path to the PostgreSQL log file')
    parser.add_argument('--patterns', type=str, required=True, help='Path to the patterns JSON file')
    parser.add_argument('--http-endpoint', type=str, required=True, help='HTTP endpoint to send events to')
    parser.add_argument('--poll-interval', type=float, default=1.0, help='Poll interval in seconds')
    
    args = parser.parse_args()
    
    # Load patterns from JSON file
    with open(args.patterns, 'r') as f:
        patterns = json.load(f)
    
    # Create and run the log monitor
    monitor = LogMonitor(
        log_file_path=args.log_file,
        patterns=patterns,
        http_endpoint=args.http_endpoint,
        db_url=settings.database_url,
        poll_interval=args.poll_interval
    )
    
    try:
        await monitor.run()
    except KeyboardInterrupt:
        print("Log monitor stopped by user")
    except Exception as e:
        print(f"Error running log monitor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 