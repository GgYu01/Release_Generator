# api/file_manager.py

"""
File Management API endpoints.

Supports uploading, downloading, and deleting files.
"""

import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
from config.settings import config
from utils.logger import get_logger
from utils.exception_handler import AppException

router = APIRouter()
logger = get_logger(__name__)


def get_full_path(relative_path: str) -> str:
    """
    Construct the full path based on the repository root directory.

    :param relative_path: Relative file path within the repository root
    :return: Absolute file system path
    """
    root_directory = config.repository_root if hasattr(config, 'repository_root') else '/home/nebula'
    full_path = os.path.abspath(os.path.join(root_directory, relative_path))
    return full_path


@router.post("/upload", summary="Upload a file")
async def upload_file(relative_path: str, file: UploadFile = File(...)):
    """
    Upload a file to the server.

    :param relative_path: Target relative path to save the file
    :param file: The file to upload
    :return: Success message
    """
    try:
        full_path = get_full_path(relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"Uploaded file to {full_path}")
        return {"message": "File uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download", summary="Download a file")
async def download_file(relative_path: str):
    """
    Download a file from the server.

    :param relative_path: Relative path of the file to download
    :return: FileResponse for the requested file
    """
    try:
        full_path = get_full_path(relative_path)
        if not os.path.exists(full_path):
            logger.error(f"File not found: {full_path}")
            raise HTTPException(status_code=404, detail="File not found")
        logger.info(f"Downloading file from {full_path}")
        return FileResponse(full_path, filename=os.path.basename(full_path))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete", summary="Delete a file")
async def delete_file(relative_path: str):
    """
    Delete a file from the server.

    :param relative_path: Relative path of the file to delete
    :return: Success message
    """
    try:
        full_path = get_full_path(relative_path)
        if not os.path.exists(full_path):
            logger.error(f"File not found for deletion: {full_path}")
            raise HTTPException(status_code=404, detail="File not found")
        os.remove(full_path)
        logger.info(f"Deleted file at {full_path}")
        return {"message": "File deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))