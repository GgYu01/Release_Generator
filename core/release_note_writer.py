# core/release_note_writer.py
"""
Release Note generation module to handle table creation and filling.
"""

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Dict
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ReleaseNoteWriter:
    """
    Generates and fills the Release Note Excel sheet.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.setup_sheet()

    def setup_sheet(self):
        """
        Sets up the initial structure of the sheet.
        """
        headers = [
            "Release Version", "Feature", "Module", "Patch",
            "Sample Code/Document Path", "Submission Info",
            "Test Leader / Modifier / MTK Owner", "Submission Time",
            "Is Ported to Another Platform?", "Is Ported and Tested?",
            "Is Released to Customer and Customer Name", "Change ID / Commit ID Title",
            "MTK Merge Date", "MTK Registration Status", "Commit Hash"
        ]
        self.sheet.append(headers)
        logger.info("Initialized Release Note sheet with headers.")

    def insert_commits(self, commits: List[Dict[str, str]]):
        """
        Inserts commit information into the sheet.

        :param commits: List of commit dictionaries.
        """
        for commit in commits:
            row = [
                commit.get("release_version", ""),
                commit.get("message", ""),
                commit.get("module", ""),
                commit.get("patch_paths", ""),
                "",
                commit.get("submission_info", ""),
                f"{settings.TEST_LEADER} / {settings.MODIFIER} / {settings.MTK_OWNER}",
                settings.SUBMISSION_TIME,
                settings.IS_PORTED,
                settings.IS_TESTED,
                settings.CUSTOMER_RELEASE,
                settings.CHANGE_ID,
                settings.MTK_MERGE_DATE,
                settings.MTK_REGISTRATION_STATUS,
                commit.get("hash", "")
            ]
            self.sheet.insert_rows(idx=2)
            self.sheet.append(row)
        logger.info(f"Inserted {len(commits)} commits into the Release Note.")

    def save(self):
        """
        Saves the workbook to the specified file path.
        """
        self.workbook.save(self.filepath)
        logger.info(f"Saved Release Note to {self.filepath}")
