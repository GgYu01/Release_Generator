# core/git_handler.py

import os
from typing import List, Dict
from git import Repo, GitCommandError
from utils.logger import get_logger
from utils.exception_handler import GitException

logger = get_logger(__name__)


class GitHandler:
    """
    Class to handle Git operations for a repository.

    Provides methods to retrieve tags and commit information.

    Attributes:
        repo_path (str): File system path to the Git repository.
        repo (Repo): GitPython Repo object representing the repository.
    """

    def __init__(self, repo_path: str):
        """
        Initialize the GitHandler with the path to the repository.

        :param repo_path: Absolute path to the Git repository.
        :raises GitException: If the repository is invalid or inaccessible.
        """
        self.repo_path = repo_path
        if not os.path.exists(repo_path):
            logger.error(f"Repository path does not exist: {repo_path}")
            raise GitException(f"Repository path does not exist: {repo_path}")
        try:
            self.repo = Repo(repo_path)
            if self.repo.bare:
                logger.error(f"Repository at {repo_path} is a bare repository")
                raise GitException(f"Repository at {repo_path} is bare")
            logger.info(f"Initialized GitHandler for repository at {repo_path}")
        except GitCommandError as e:
            logger.error(f"Git command error for repository at {repo_path}: {e}")
            raise GitException(f"Git command error: {e}") from e

    def get_latest_tags(self, n: int = 2) -> List[str]:
        """
        Retrieve the latest n tags in the repository.

        :param n: Number of tags to retrieve (default is 2).
        :return: List of tag names, ordered from latest to oldest.
        :raises GitException: If unable to retrieve tags.
        """
        try:
            tags = sorted(
                self.repo.tags,
                key=lambda t: t.commit.committed_datetime,
                reverse=True
            )
            latest_tags = [tag.name for tag in tags[:n]]
            logger.debug(f"Latest {n} tags in {self.repo_path}: {latest_tags}")
            return latest_tags
        except Exception as e:
            logger.error(f"Error retrieving tags: {e}")
            raise GitException(f"Error retrieving tags: {e}") from e

    def get_commits_between_tags(self, older_tag: str, newer_tag: str) -> List[Dict]:
        """
        Get a list of commits between two tags.

        :param older_tag: The older tag name (starting point, exclusive).
        :param newer_tag: The newer tag name (ending point, inclusive).
        :return: List of commit dictionaries with commit details.
        :raises GitException: If unable to retrieve commits.
        """
        try:
            commit_range = f"{older_tag}..{newer_tag}"
            commits = list(self.repo.iter_commits(commit_range))
            commit_list = []
            for commit in commits:
                commit_info = {
                    'commit_id': commit.hexsha,
                    'author': commit.author.name,
                    'date': commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    'message': commit.message.strip(),
                }
                commit_list.append(commit_info)
            logger.debug(f"Found {len(commit_list)} commits between {older_tag} and {newer_tag}")
            return commit_list
        except Exception as e:
            logger.error(f"Error retrieving commits between tags: {e}")
            raise GitException(f"Error retrieving commits: {e}") from e

    # Additional Git operation methods can be added here