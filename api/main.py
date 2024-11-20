# -*- coding: utf-8 -*-

"""
FastAPI application entry point for providing HTTP interfaces.
"""

import uvicorn
from fastapi import FastAPI
from api.file_manager import router as file_router
from api.task_manager import router as task_router
from config.settings import Settings

app = FastAPI()

app.include_router(file_router, prefix="/files")
app.include_router(task_router, prefix="/tasks")

settings = Settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
