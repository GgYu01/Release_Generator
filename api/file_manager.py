# -*- coding: utf-8 -*-

"""
FastAPI router for file upload, download, and deletion.
"""

import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from utils.file_utils import save_upload_file
from config.settings import Settings

router = APIRouter()
settings = Settings()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    save_path = os.path.join(settings.grt_path, file.filename)
    await save_upload_file(file, save_path)
    return {"filename": file.filename}

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(settings.grt_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join(settings.grt_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"detail": "File deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")
