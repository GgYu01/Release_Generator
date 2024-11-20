# -*- coding: utf-8 -*-

"""
Module for processing commit information between two tags.
"""

import os
from utils.logger import logger
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser
from typing import List, Dict

class CommitProcessor:
    def __init__(self, settings, git_handler: GitHandler, manifest_parser: ManifestParser):
        self.settings = settings
        self.git_handler = git_handler
        self.manifest_parser = manifest_parser

    def get_all_commits_info(self, repositories: List[tuple], latest_tag: str, second_latest_tag: str) -> List[Dict]:
        """
        Get commit messages and hashes between two tags for all repositories,
        excluding commits with special messages in specific paths.
        """
        all_commits_info = []
        for repo_name, repo_path in repositories:
            logger.info(f"Processing repository: {repo_name} at {repo_path}")
            commits = self.git_handler.get_commits_between_tags(repo_path, second_latest_tag, latest_tag)
            for commit_hash in commits:
                message = self.git_handler.get_commit_message(repo_path, commit_hash)
                # Check for special commit messages in specific paths
                if self._is_special_commit(repo_path, message):
                    logger.debug(f"Excluded commit {commit_hash} with message: {message}")
                    # Associate patch to nebula and grpower if needed
                    all_commits_info.append({
                        'hash': commit_hash,
                        'message': message,
                        'repo': repo_name,
                        'is_special': True
                    })
                else:
                    all_commits_info.append({
                        'hash': commit_hash,
                        'message': message,
                        'repo': repo_name,
                        'is_special': False
                    })
        logger.info(f"Total commits collected: {len(all_commits_info)}")
        return all_commits_info

    def _is_special_commit(self, repo_path: str, message: str) -> bool:
        """
        Determine if a commit message contains any special filters.
        """
        special_paths = [
            self.settings.grt_path,
            os.path.join(self.settings.alps_path, 'vendor/mediatek/proprietary/trustzone/grt')
        ]
        if repo_path in special_paths:
            for filter_str in self.settings.special_commit_filters:
                if filter_str in message:
                    return True
        return False
