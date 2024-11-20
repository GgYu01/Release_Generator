# utils/file_utils.py
"""
File operation utility functions.
"""

import os
from utils.logger import get_logger

logger = get_logger(__name__)


def remove_file(file_path: str):
    """
    Removes a file if it exists.

    :param file_path: Path to the file.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info(f"Removed file: {file_path}")
    else:
        logger.warning(f"File not found: {file_path}")
