# core/git_handler.py
"""
Git operation module that encapsulates repo, jiri, and git commands.
"""

import subprocess
from typing import List
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class GitHandler:
    """
    Handles Git operations for various tools.
    """

    def __init__(self):
        self.repositories = settings.REPOSITORIES

    def get_latest_tags(self, repo_path: str) -> List[str]:
        """
        Retrieves the latest and second latest tags from a Git repository.

        :param repo_path: Path to the Git repository.
        :return: A list containing the latest and second latest tag names.
        """
        try:
            cmd = ["git", "-C", repo_path, "tag", "--sort=-creatordate"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            tags = result.stdout.strip().split('\n')
            return tags[:2]  # Latest and second latest tags
        except subprocess.CalledProcessError as e:
            logger.error(f"Error retrieving tags from {repo_path}: {e}")
            return []

    def generate_patches(self, repo_path: str, old_tag: str, new_tag: str) -> List[str]:
        """
        Generates patch files between two tags.

        :param repo_path: Path to the Git repository.
        :param old_tag: The older tag.
        :param new_tag: The newer tag.
        :return: List of generated patch file paths.
        """
        try:
            cmd = ["git", "-C", repo_path, "format-patch", f"{old_tag}..{new_tag}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            patches = result.stdout.strip().split('\n')
            logger.info(f"Generated patches in {repo_path}: {patches}")
            return patches
        except subprocess.CalledProcessError as e:
            logger.error(f"Error generating patches in {repo_path}: {e}")
            return []

    def get_commits_between_tags(self, repo_path: str, old_tag: str, new_tag: str) -> List[dict]:
        """
        Retrieves commit information between two tags.

        :param repo_path: Path to the Git repository.
        :param old_tag: The older tag.
        :param new_tag: The newer tag.
        :return: List of commit dictionaries.
        """
        try:
            cmd = [
                "git", "-C", repo_path, "log",
                f"{old_tag}..{new_tag}", "--pretty=format:%H%n%s%n%b%n==END=="
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            commits_raw = result.stdout.strip().split('==END==\n')
            commits = []
            for commit_raw in commits_raw:
                lines = commit_raw.strip().split('\n')
                if len(lines) >= 2:
                    commit = {
                        "hash": lines[0],
                        "message": '\n'.join(lines[1:])
                    }
                    commits.append(commit)
            logger.info(f"Retrieved {len(commits)} commits from {repo_path}")
            return commits
        except subprocess.CalledProcessError as e:
            logger.error(f"Error retrieving commits from {repo_path}: {e}")
            return []
