# utils/logger.py
"""
Logging module.
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger.

    :param name: Name of the logger.
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(name)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
