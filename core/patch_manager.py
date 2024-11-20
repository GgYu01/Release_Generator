# -*- coding: utf-8 -*-

"""
Module for managing patch files.
"""

import os
from utils.logger import logger
from utils.exception_handler import PatchManagementException
from typing import List, Dict
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser

class PatchManager:
    def __init__(self, settings, git_handler: GitHandler, manifest_parser: ManifestParser):
        self.settings = settings
        self.git_handler = git_handler
        self.manifest_parser = manifest_parser

    def generate_and_associate_patches(self, repositories: List[tuple], latest_tag: str, second_latest_tag: str, commits_info: List[Dict]) -> Dict[str, List[str]]:
        """
        Generate patches and associate them with commits.
        Returns a dictionary mapping commit hashes to their patch file paths.
        """
        patch_mapping = {}
        for repo_name, repo_path in repositories:
            logger.info(f"Generating patches for repository: {repo_name} at {repo_path}")
            try:
                patches = self.git_handler.generate_patches(repo_path, second_latest_tag, latest_tag)
                for patch in patches:
                    commit_hash = self._extract_commit_hash_from_patch(patch, repo_path)
                    if commit_hash:
                        # Check if this commit is marked as special
                        commit_info = next((c for c in commits_info if c['hash'] == commit_hash), None)
                        if commit_info and commit_info['is_special']:
                            # Associate with nebula and grpower
                            patch_mapping.setdefault('nebula', []).append(patch)
                            patch_mapping.setdefault('grpower', []).append(patch)
                        else:
                            patch_mapping.setdefault(commit_hash, []).append(patch)
            except PatchManagementException as e:
                logger.error(f"Error generating patches for {repo_name}: {e}")
        logger.info(f"Total patches generated and associated: {len(patch_mapping)}")
        return patch_mapping

    def _extract_commit_hash_from_patch(self, patch_path: str, repo_path: str) -> str:
        """
        Extract the commit hash from a patch file.
        Assumes the commit hash is present in the patch file name or content.
        """
        try:
            with open(patch_path, 'r') as f:
                for line in f:
                    if line.startswith('From '):
                        parts = line.split()
                        if len(parts) >= 2:
                            commit_hash = parts[1]
                            logger.debug(f"Extracted commit hash {commit_hash} from {patch_path}")
                            return commit_hash
        except Exception as e:
            logger.error(f"Failed to extract commit hash from {patch_path}: {e}")
        return ""

    def clean_patches(self, repositories: List[tuple]):
        """
        Clean up patch files in all repositories.
        """
        try:
            for repo_name, repo_path in repositories:
                patches = [f for f in os.listdir(repo_path) if f.endswith('.patch')]
                for patch in patches:
                    patch_full_path = os.path.join(repo_path, patch)
                    os.remove(patch_full_path)
                    logger.debug(f"Removed patch file: {patch_full_path}")
            logger.info("Cleaned up all patch files")
        except Exception as e:
            logger.error(f"Failed to clean patches: {e}")
            raise PatchManagementException(f"Failed to clean patches: {e}")
