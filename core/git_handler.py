# -*- coding: utf-8 -*-

"""
Module for handling Git operations, including repo and jiri commands.
"""

import subprocess
import os
from utils.logger import logger
from utils.exception_handler import GitOperationException
from typing import Tuple, List, Dict
import re

class GitHandler:
    def __init__(self, settings):
        self.settings = settings

    def get_grt_tags(self) -> Tuple[str, str]:
        """
        Get the latest and second latest tags from the grt repository.
        """
        try:
            cmd = ['git', 'tag', '--list', 'release-spm.mt8678_*']
            tags = subprocess.check_output(cmd, cwd=self.settings.grt_path).decode().splitlines()
            # Filter tags that match the expected pattern
            pattern = re.compile(r'release-spm\.mt8678(?:_mt8676)?_\d{4}_\d{4}_\d{2}')
            filtered_tags = [tag for tag in tags if pattern.match(tag)]
            if len(filtered_tags) < 2:
                logger.error("Not enough tags found in grt repository.")
                raise GitOperationException("Not enough tags found in grt repository.")
            # Sort tags based on date identifier
            tags_sorted = sorted(filtered_tags, key=self._tag_sort_key, reverse=True)
            latest_tag = tags_sorted[0]
            second_latest_tag = tags_sorted[1]
            logger.info(f"Latest tags in grt: {latest_tag}, {second_latest_tag}")
            return latest_tag, second_latest_tag
        except Exception as e:
            logger.error(f"Failed to get tags from grt repository: {e}")
            raise GitOperationException("Failed to get tags from grt repository")

    def _tag_sort_key(self, tag: str):
        """
        Custom sort key for tags based on date and identifier.
        """
        parts = tag.split('_')
        # Extract date identifier parts
        if 'mt8676' in tag:
            date_parts = parts[3:6]  # release-spm.mt8678_mt8676_<date_part>
        else:
            date_parts = parts[2:5]  # release-spm.mt8678_<date_part>
        date_numeric_str = ''.join(date_parts)
        # Ensure the date_numeric_str is numeric
        if not date_numeric_str.isdigit():
            logger.warning(f"Non-numeric date identifier found in tag: {tag}")
            return 0  # Assign lowest priority to invalid tags
        date_numeric = int(date_numeric_str)
        return date_numeric

    def construct_tag_for_repo(self, base_tag: str, repo_path: str) -> str:
        """
        Construct a tag for a repository based on the base tag from grt.
        Automatically adds 'mt8676' prefix for nebula sub-repositories.
        """
        # 判断仓库是否在nebula_path下
        if os.path.commonpath([repo_path, self.settings.nebula_path]) == self.settings.nebula_path:
            parts = base_tag.split('_')
            if 'mt8676' in base_tag:
                # 标签格式为 release-spm.mt8678_mt8676_<年份>_<月日>_<编号>
                if len(parts) >= 5:
                    date_id = '_'.join(parts[2:])  # 包含年份
                    return f"release-spm.mt8678_mt8676_{date_id}"
                else:
                    logger.warning(f"Tag format unexpected for repo {repo_path}. Using base tag.")
                    return base_tag
            else:
                # 标签格式为 release-spm.mt8678_<年份>_<月日>_<编号>
                if len(parts) >= 4:
                    date_id = '_'.join(parts[2:])
                    return f"release-spm.mt8678_mt8676_{date_id}"
                else:
                    logger.warning(f"Tag format unexpected for repo {repo_path}. Using base tag.")
                    return base_tag
        else:
            return base_tag

    def get_commits_between_tags(self, repo_path: str, start_tag: str, end_tag: str) -> List[str]:
        """
        Get commit hashes between two tags.
        """
        try:
            cmd = ['git', 'log', f'{start_tag}..{end_tag}', '--pretty=format:%H']
            commits = subprocess.check_output(cmd, cwd=repo_path).decode().splitlines()
            logger.info(f"Found {len(commits)} commits between {start_tag} and {end_tag} in {repo_path}")
            return commits
        except Exception as e:
            logger.error(f"Failed to get commits from {repo_path}: {e}")
            raise GitOperationException(f"Failed to get commits from {repo_path}")

    def generate_patches(self, repo_path: str, start_tag: str, end_tag: str) -> List[str]:
        """
        Generate patch files between two tags in the repository root.
        Returns a list of generated patch file paths.
        """
        try:
            # Remove existing patch files to avoid duplication
            existing_patches = [f for f in os.listdir(repo_path) if f.endswith('.patch')]
            for patch in existing_patches:
                os.remove(os.path.join(repo_path, patch))
                logger.debug(f"Removed existing patch file: {patch}")
            # Generate patches
            cmd = ['git', 'format-patch', f'{start_tag}..{end_tag}']
            subprocess.check_call(cmd, cwd=repo_path)
            patches = sorted([f for f in os.listdir(repo_path) if f.endswith('.patch')])
            patch_paths = [os.path.join(repo_path, patch) for patch in patches]
            logger.info(f"Generated {len(patch_paths)} patches in {repo_path}")
            return patch_paths
        except Exception as e:
            logger.error(f"Failed to generate patches in {repo_path}: {e}")
            raise GitOperationException(f"Failed to generate patches in {repo_path}")

    def get_commit_message(self, repo_path: str, commit_hash: str) -> str:
        """
        Get the commit message for a specific commit.
        """
        try:
            cmd = ['git', 'show', '-s', '--format=%s', commit_hash]
            message = subprocess.check_output(cmd, cwd=repo_path).decode().strip()
            logger.debug(f"Commit {commit_hash} message: {message}")
            return message
        except Exception as e:
            logger.error(f"Failed to get commit message from {repo_path}: {e}")
            raise GitOperationException(f"Failed to get commit message from {repo_path}")

    def get_last_commit_id(self, repo_path: str) -> str:
        """
        Get the latest commit ID from the repository.
        """
        try:
            cmd = ['git', 'rev-parse', 'HEAD']
            commit_id = subprocess.check_output(cmd, cwd=repo_path).decode().strip()
            logger.info(f"Latest commit in {repo_path}: {commit_id}")
            return commit_id
        except Exception as e:
            logger.error(f"Failed to get latest commit ID from {repo_path}: {e}")
            raise GitOperationException(f"Failed to get latest commit ID from {repo_path}")

    def get_latest_tags_for_repo(self, repo_path: str) -> Tuple[str, str]:
        """
        Get the latest and second latest tags for a repository based on its tag pattern.
        """
        if os.path.commonpath([repo_path, self.settings.nebula_path]) == self.settings.nebula_path:
            # nebula sub-repository tag pattern
            tag_pattern = 'release-spm.mt8678_mt8676_*'
            pattern = re.compile(r'release-spm\.mt8678_mt8676_\d{4}_\d{4}_\d{2}')
        else:
            # other repositories tag pattern
            tag_pattern = 'release-spm.mt8678_*'
            pattern = re.compile(r'release-spm\.mt8678_\d{4}_\d{4}_\d{2}')

        try:
            cmd = ['git', 'tag', '--list', tag_pattern]
            tags = subprocess.check_output(cmd, cwd=repo_path).decode().splitlines()
            # Filter tags that match the expected pattern
            filtered_tags = [tag for tag in tags if pattern.match(tag)]
            if len(filtered_tags) < 2:
                logger.error(f"Not enough tags found in repository {repo_path}.")
                raise GitOperationException(f"Not enough tags found in repository {repo_path}.")
            # Sort tags based on date identifier
            tags_sorted = sorted(filtered_tags, key=self._tag_sort_key, reverse=True)
            latest_tag = tags_sorted[0]
            second_latest_tag = tags_sorted[1]
            logger.info(f"Latest tags in {repo_path}: {latest_tag}, {second_latest_tag}")
            return latest_tag, second_latest_tag
        except Exception as e:
            logger.error(f"Failed to get tags from repository {repo_path}: {e}")
            raise GitOperationException(f"Failed to get tags from repository {repo_path}")
