# core/commit_processor.py

import os
from typing import List, Dict, Any
from config.settings import config, RepositoryConfig
from core.git_handler import GitHandler
from utils.logger import get_logger
from utils.exception_handler import AppException

logger = get_logger(__name__)


class CommitProcessor:
    """
    Class to process commits between tags across multiple repositories.

    Attributes:
        repositories (List[RepositoryConfig]): List of repository configurations.
        special_keywords (List[str]): Keywords to identify special commits.
        commit_data (Dict[str, List[Dict]]): Processed commit data for each repository.
    """

    def __init__(self, repositories: List[RepositoryConfig]):
        """
        Initialize the CommitProcessor with repository configurations.

        :param repositories: List of RepositoryConfig instances.
        """
        self.repositories = repositories
        # Special commit identification keywords
        self.special_keywords = [
            '] thyp-sdk: ',
            '] nebula-sdk: ',
            '] tee: '
        ]
        # Dictionary to store processed commits
        self.commit_data = {}

    def process_all_commits(self) -> None:
        """
        Process commits for all repositories.

        This method iterates through all configured repositories, retrieves commits
        between the latest and second latest tags, and processes each commit.
        """
        for repo_config in self.repositories:
            logger.info(f"Processing repository: {repo_config.name}")
            try:
                self.process_repository_commits(repo_config)
            except AppException as e:
                logger.error(f"Error processing repository {repo_config.name}: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error processing repository {repo_config.name}: {e}")

    def process_repository_commits(self, repo_config: RepositoryConfig) -> None:
        """
        Process commits for a single repository.

        :param repo_config: RepositoryConfig object containing repository details.
        """
        # Initialize GitHandler for the repository
        git_handler = GitHandler(repo_config.path)
        # Retrieve the latest and second latest tags
        latest_tags = git_handler.get_latest_tags(2)
        if len(latest_tags) < 2:
            logger.warning(f"Repository {repo_config.name} does not have enough tags to process.")
            return
        repo_config.latest_tag = latest_tags[0]
        repo_config.second_latest_tag = latest_tags[1]
        logger.debug(f"Latest tags for {repo_config.name}: {latest_tags}")

        # Get commits between the two tags
        commits = git_handler.get_commits_between_tags(
            repo_config.second_latest_tag,
            repo_config.latest_tag
        )
        logger.info(f"Found {len(commits)} commits in repository {repo_config.name}.")

        # Process each commit
        processed_commits = self.process_commits(commits, repo_config)
        # Store processed commits
        self.commit_data[repo_config.name] = processed_commits

    def process_commits(self, commits: List[Dict[str, Any]], repo_config: RepositoryConfig) -> List[Dict[str, Any]]:
        """
        Process a list of commits for a repository.

        :param commits: List of commit dictionaries from GitHandler.
        :param repo_config: RepositoryConfig object.
        :return: List of processed commit dictionaries.
        """
        processed_commits = []
        for commit in commits:
            # Determine if the commit is special
            is_special = self.is_special_commit(commit['message'])
            # Map repository to module name
            module_name = self.get_module_name(commit, repo_config, is_special)
            # Prepare processed commit data
            processed_commit = {
                'repository': repo_config.name,
                'module': module_name,
                'commit_id': commit['commit_id'],
                'author': commit['author'],
                'date': commit['date'],
                'message': commit['message'],
                'is_special': is_special,
                'patch_needed': self.is_patch_needed(repo_config, is_special),
            }
            processed_commits.append(processed_commit)
            logger.debug(f"Processed commit {commit['commit_id']} from {repo_config.name}")
        return processed_commits

    def is_special_commit(self, message: str) -> bool:
        """
        Check if a commit message contains any special keywords.

        :param message: Commit message string.
        :return: True if special, False otherwise.
        """
        for keyword in self.special_keywords:
            if keyword in message:
                logger.debug(f"Commit message '{message}' is identified as special.")
                return True
        return False

    def get_module_name(self, commit: Dict[str, Any], repo_config: RepositoryConfig, is_special: bool) -> str:
        """
        Determine the module name for a commit.

        :param commit: Commit dictionary.
        :param repo_config: RepositoryConfig object.
        :param is_special: Boolean indicating if the commit is special.
        :return: Module name string.
        """
        if is_special:
            # Map special commits to 'grpower' or 'nebula' based on keywords
            message = commit['message']
            if '] thyp-sdk: ' in message or '] nebula-sdk: ' in message:
                return 'grpower'
            elif '] tee: ' in message:
                return 'nebula'
            else:
                return 'unknown'
        else:
            # Map repository name to module name
            return self.map_repository_to_module(repo_config.name)

    def map_repository_to_module(self, repo_name: str) -> str:
        """
        Map repository names to module names.

        :param repo_name: Repository name string.
        :return: Module name string.
        """
        mapping = {
            'grpower': 'nebula-hyper',
            'nebula': 'nebula-hyper',
            'grt': 'thyp-sdk',
            'grt_be': 'thyp-sdk-be',
            'alps': 'alps',
            'yocto': 'yocto',
        }
        return mapping.get(repo_name, 'unknown')

    def is_patch_needed(self, repo_config: RepositoryConfig, is_special: bool) -> bool:
        """
        Determine if a patch file needs to be generated for a commit.

        :param repo_config: RepositoryConfig object.
        :param is_special: Boolean indicating if the commit is special.
        :return: True if patch is needed, False otherwise.
        """
        # According to the requirements, patches are not generated for 'grpower' and 'nebula'
        if repo_config.name in ['grpower', 'nebula']:
            return False
        # For special commits, patches are included in 'grpower' or 'nebula' patches
        if is_special:
            return False
        # For other repositories, patches are needed
        return True

    def get_commit_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the processed commit data.

        :return: Dictionary mapping repository names to lists of processed commits.
        """
        return self.commit_data