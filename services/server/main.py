from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import subprocess
from contextlib import asynccontextmanager
import os
import sys
from pathlib import Path
from routes.route_handler import router
from utils.env import env

# Use uvicorn's logger for consistent formatting
logger = logging.getLogger("uvicorn")


# Run database migrations on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Determine base directory and environment
        is_docker = os.path.exists("/app/server")
        base_dir = (
            "/app"
            if is_docker
            else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Check if database URL is set
        if not env.database_url:
            logger.warning("Database URL is not set, migrations will not be run")
            yield
            return

        # Set schema path to configured location
        schema_path = os.path.join(base_dir, env.schema_file)
        migrations_dir = os.path.join(base_dir, env.migrations_dir)

        # Run database migrations
        logger.info(f"Running database migrations from directory: {migrations_dir}")
        logger.info(f"Schema will be updated at: {schema_path}")
        result = subprocess.run(
            [
                "dbmate",
                "--migrations-dir",
                migrations_dir,
                "--schema-file",
                schema_path,
                "up",
            ],
            capture_output=True,
            text=True,
            env=os.environ,
        )

        if result.returncode == 0:
            logger.info("Database migrations completed successfully")
        else:
            logger.error(f"Error running database migrations: {result.stderr}")

    except Exception as e:
        logger.error(f"Failed to run database migrations: {e}")

    yield  # Application execution
    # No cleanup needed


app = FastAPI(title="Simple FastAPI Server", lifespan=lifespan)

# Configure CORS using environment settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned routes
app.include_router(router, prefix="/api")


# Add root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Simple FastAPI Server"}


if __name__ == "__main__":
    import uvicorn

    # When running directly with python -m, use the environment settings
    uvicorn.run("main:app", host=env.host, port=env.port, reload=env.debug)
