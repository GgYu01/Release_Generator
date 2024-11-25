from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

def init_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"}
        )