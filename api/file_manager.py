from fastapi import APIRouter, UploadFile, File, Response
from typing import List
from pathlib import Path

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> dict:
    file_location = Path("uploads") / file.filename
    with file_location.open("wb") as f:
        content = await file.read()
        f.write(content)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.get("/download/{file_name}")
async def download_file(file_name: str) -> Response:
    file_location = Path("uploads") / file_name
    if file_location.exists():
        return Response(content=file_location.read_bytes(), media_type='application/octet-stream')
    else:
        return Response(status_code=404)

@router.delete("/delete/{file_name}")
async def delete_file(file_name: str) -> dict:
    file_location = Path("uploads") / file_name
    if file_location.exists():
        file_location.unlink()
        return {"info": f"file '{file_name}' deleted"}
    else:
        return {"error": "file not found"}