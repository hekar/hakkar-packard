from sqlalchemy import create_engine, text
from metrum.settings import settings

def run_migration():
    """Create the log_events table."""
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        # Check if table exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'log_events'
            );
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            # Create the log_events table
            conn.execute(text("""
                CREATE TABLE log_events (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    query_text TEXT,
                    explain_text TEXT,
                    duration_ms FLOAT,
                    pattern_name VARCHAR(255),
                    status VARCHAR(50) NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX idx_log_events_timestamp ON log_events(timestamp);
                CREATE INDEX idx_log_events_status ON log_events(status);
                CREATE INDEX idx_log_events_pattern_name ON log_events(pattern_name);
            """))
            conn.commit()
            print("Created log_events table")
        else:
            print("log_events table already exists")

if __name__ == "__main__":
    run_migration() 