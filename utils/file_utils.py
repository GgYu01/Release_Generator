# -*- coding: utf-8 -*-

"""
Utility functions for file operations.
"""

import shutil
from fastapi import UploadFile
from utils.logger import logger

async def save_upload_file(upload_file: UploadFile, destination: str):
    try:
        with open(destination, 'wb') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        logger.info(f"File saved to {destination}")
    except Exception as e:
        logger.error(f"Failed to save file {destination}: {e}")
        raise
    finally:
        await upload_file.close()
