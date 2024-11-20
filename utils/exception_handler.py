# utils/exception_handler.py
"""
Exception handling module.
"""

import traceback
from utils.logger import get_logger

logger = get_logger(__name__)


def handle_exception(e: Exception):
    """
    Logs the exception traceback.

    :param e: Exception instance.
    """
    logger.error(f"An exception occurred: {e}")
    logger.error(traceback.format_exc())
