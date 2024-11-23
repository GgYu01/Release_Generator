# utils/logger.py

import logging
from config.settings import config


def setup_logger():
    """
    Set up the logging configuration based on settings in config.
    """
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)
    log_format = config.log_format
    logging.basicConfig(level=log_level, format=log_format)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    :param name: Name of the logger, usually __name__
    :return: Configured logger instance
    """
    return logging.getLogger(name)


# Initialize the logger configuration when the module is imported
setup_logger()