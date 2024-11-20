# core/patch_manager.py
"""
Patch file management module, including generation, cleanup, and path handling.
"""

import os
from typing import List
from core.git_handler import GitHandler
from config import settings
from utils.file_utils import remove_file
from utils.logger import get_logger

logger = get_logger(__name__)


class PatchManager:
    """
    Manages patch files.
    """

    def __init__(self):
        self.git_handler = GitHandler()
        self.generated_patches = []

    def generate_patches_for_repo(self, repo_path: str, old_tag: str, new_tag: str) -> List[str]:
        """
        Generates patches for a specific repository.

        :param repo_path: Repository path.
        :param old_tag: Older tag.
        :param new_tag: Newer tag.
        :return: List of patch file paths.
        """
        patches = self.git_handler.generate_patches(repo_path, old_tag, new_tag)
        self.generated_patches.extend([os.path.join(repo_path, p) for p in patches])
        return patches

    def cleanup_patches(self):
        """
        Cleans up generated patch files.
        """
        for patch in self.generated_patches:
            remove_file(patch)
            logger.info(f"Removed patch file: {patch}")
        self.generated_patches = []
