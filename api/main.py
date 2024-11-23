# api/main.py

"""
Main module to run the FastAPI application.
"""

import uvicorn
from fastapi import FastAPI
from api import file_manager, task_manager
from config.settings import config
from utils.logger import get_logger

app = FastAPI(
    title="Release Note Generator API",
    description="API endpoints for file and task management",
    version="1.0.0",
)

# Include routers from different modules
app.include_router(file_manager.router, prefix="/files", tags=["File Management"])
app.include_router(task_manager.router, prefix="/tasks", tags=["Task Management"])

logger = get_logger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the FastAPI application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the FastAPI application")


if __name__ == "__main__":
    # Retrieve host and port from configuration or use defaults
    host = config.api_host if hasattr(config, 'api_host') else "127.0.0.1"
    port = config.api_port if hasattr(config, 'api_port') else 8000
    uvicorn.run(app, host=host, port=port)