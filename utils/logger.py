# -*- coding: utf-8 -*-

"""
Logging module for the Release Note Generator script.
"""

import logging
from config.settings import Settings

def get_logger():
    settings = Settings()

    logger = logging.getLogger('ReleaseNoteGenerator')
    logger.setLevel(getattr(logging, settings.log_level.upper(), 'INFO'))

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = get_logger()
