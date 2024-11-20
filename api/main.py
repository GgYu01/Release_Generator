# api/main.py
"""
FastAPI application entry point.
"""

import uvicorn
from fastapi import FastAPI
from config import settings
from api.file_manager import router as file_router
from api.task_manager import router as task_router
from utils.logger import get_logger

logger = get_logger(__name__)
app = FastAPI()

app.include_router(file_router, prefix="/files")
app.include_router(task_router, prefix="/tasks")


if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
