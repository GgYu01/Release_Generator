# api/file_manager.py
"""
File upload, download, and delete interfaces.
"""

import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server.

    :param file: File to upload.
    """
    file_location = os.path.join(settings.GRPOWER_PATH, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    logger.info(f"Uploaded file: {file_location}")
    return {"info": f"File '{file.filename}' uploaded successfully."}


@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """
    Downloads a file from the server.

    :param file_path: Relative path to the file.
    """
    absolute_path = os.path.join(settings.GRPOWER_PATH, file_path)
    if os.path.isfile(absolute_path):
        logger.info(f"Downloading file: {absolute_path}")
        return FileResponse(absolute_path)
    else:
        logger.error(f"File not found: {absolute_path}")
        raise HTTPException(status_code=404, detail="File not found")


@router.delete("/delete/{file_path:path}")
async def delete_file(file_path: str):
    """
    Deletes a file from the server.

    :param file_path: Relative path to the file.
    """
    absolute_path = os.path.join(settings.GRPOWER_PATH, file_path)
    if os.path.isfile(absolute_path):
        os.remove(absolute_path)
        logger.info(f"Deleted file: {absolute_path}")
        return {"info": f"File '{file_path}' deleted successfully."}
    else:
        logger.error(f"File not found: {absolute_path}")
        raise HTTPException(status_code=404, detail="File not found")
