from fastapi import FastAPI
from config.settings import settings
from api.file_manager import router as file_router
from api.task_manager import router as task_router

app = FastAPI()

app.include_router(file_router, prefix="/files")
app.include_router(task_router, prefix="/tasks")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_settings['host'], port=settings.api_settings['port'], debug=settings.api_settings['debug'])