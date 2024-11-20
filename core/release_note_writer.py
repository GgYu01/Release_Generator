# -*- coding: utf-8 -*-

"""
Module for generating and updating the Release Note Excel sheet.
"""

import openpyxl
from openpyxl.utils import get_column_letter
from utils.logger import logger
from utils.exception_handler import ReleaseNoteException
from core.git_handler import GitHandler
from typing import List, Dict, Tuple
import os

class ReleaseNoteWriter:
    def __init__(self, settings, git_handler: GitHandler):
        self.settings = settings
        self.git_handler = git_handler
        self.excel_file = 'Release_Notes.xlsx'
        if not os.path.exists(self.excel_file):
            self._create_excel()

    def _create_excel(self):
        """
        Create a new Excel file with headers if it does not exist.
        """
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        headers = [
            'Release Version', 'Feature', 'Module', 'Patch Path',
            'Example Code/Doc Path', 'Commit Info', 'Tester / Modifier / MTK Owner',
            'Submission Time', 'Porting Required', 'Porting Status',
            'Release Customer', 'Change ID', 'MTK Merge Date',
            'MTK Registration Status', 'Commit ID'
        ]
        sheet.append(headers)
        workbook.save(self.excel_file)
        logger.info(f"Created new Excel file with headers: {self.excel_file}")

    def insert_rows(self, workbook, num_rows: int):
        """
        Insert rows at the specified position.
        """
        sheet = workbook.active
        sheet.insert_rows(2, num_rows)
        logger.debug(f"Inserted {num_rows} rows at position 2")
        return sheet

    def fill_data(self, sheet, commits_info: List[Dict], constructed_tags: Dict[str, Tuple[str, str]], patch_mapping: Dict[str, List[str]]):
        """
        Fill the Excel sheet with commit information.
        """
        row_num = 2
        for commit_info in commits_info:
            repo_path = commit_info['repo']
            if repo_path in constructed_tags:
                latest_tag = constructed_tags[repo_path][0]
            else:
                latest_tag = "Unknown_Tag"

            if commit_info['is_special']:
                # Associate patch with nebula and grpower
                patch_paths = patch_mapping.get('nebula', []) + patch_mapping.get('grpower', [])
                formatted_patches = self._format_patch_paths(patch_paths)
                module = 'nebula-hyper'
            else:
                patch_paths = patch_mapping.get(commit_info['hash'], [])
                formatted_patches = self._format_patch_paths(patch_paths)
                module = self.determine_module(repo_path)

            # Column F: Commit Info
            zircon_commit = self.git_handler.get_last_commit_id(self.settings.zircon_repo)
            garnet_commit = self.git_handler.get_last_commit_id(self.settings.garnet_repo)
            commit_info_f = f"zircon: {zircon_commit}\ngarnet: {garnet_commit}"

            # Populate Excel row
            sheet.cell(row=row_num, column=1, value=latest_tag)  # Release Version
            sheet.cell(row=row_num, column=2, value=commit_info['message'])  # Feature
            sheet.cell(row=row_num, column=3, value=module)  # Module
            sheet.cell(row=row_num, column=4, value=formatted_patches)  # Patch Path
            # Column E is left empty
            sheet.cell(row=row_num, column=6, value=commit_info_f)  # Commit Info
            sheet.cell(row=row_num, column=7, value=f"{self.settings.tester} / {self.settings.modifier} / {self.settings.mtk_owner}")
            sheet.cell(row=row_num, column=8, value=self.settings.submission_time)
            sheet.cell(row=row_num, column=9, value=self.settings.porting_required)
            sheet.cell(row=row_num, column=10, value=self.settings.porting_status)
            sheet.cell(row=row_num, column=11, value=self.settings.release_customer)
            sheet.cell(row=row_num, column=12, value=self.settings.change_id)
            sheet.cell(row=row_num, column=13, value=self.settings.mtk_merge_date)
            sheet.cell(row=row_num, column=14, value=self.settings.mtk_registration_status)
            sheet.cell(row=row_num, column=15, value=commit_info['hash'])  # Commit ID
            row_num += 1
            logger.debug(f"Filled data for commit {commit_info['hash']} at row {row_num}")

    def _format_patch_paths(self, patches: List[str]) -> str:
        """
        Format patch paths by removing '/home/nebula/' and joining with newline.
        """
        formatted_patches = [patch.replace('/home/nebula/', '') for patch in patches]
        return '\n'.join(formatted_patches)

    def determine_module(self, repo_name: str) -> str:
        """
        Determine the module based on the repository name.
        """
        if repo_name in ['nebula', 'grpower']:
            return 'nebula-hyper'
        elif repo_name == 'alps':
            return 'alps'
        elif repo_name == 'yocto':
            return 'yocto'
        elif repo_name == 'grt':
            return 'thyp-sdk'
        elif repo_name == 'grt_be':
            return 'thyp-sdk-be'
        else:
            return 'unknown'

    def save_excel(self, workbook):
        """
        Save the updated Excel workbook.
        """
        try:
            workbook.save(self.excel_file)
            logger.info(f"Release Note saved to {self.excel_file}")
        except Exception as e:
            logger.error(f"Failed to save Excel file: {e}")
            raise ReleaseNoteException("Failed to save Excel file")

    def update_release_note(self, commits_info: List[Dict], constructed_tags: Dict[str, Tuple[str, str]], patch_mapping: Dict[str, List[str]]):
        """
        Update the release note Excel sheet with the provided commit information and patch mappings.
        """
        try:
            workbook = openpyxl.load_workbook(self.excel_file)
            num_commits = len(commits_info)
            sheet = self.insert_rows(workbook, num_commits)
            self.fill_data(sheet, commits_info, constructed_tags, patch_mapping)
            self.save_excel(workbook)
        except Exception as e:
            logger.error(f"Failed to update release note: {e}")
            raise ReleaseNoteException("Failed to update release note")
