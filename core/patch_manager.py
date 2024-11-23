# core/patch_manager.py

import os
import shutil
import subprocess
from typing import List, Dict
from config.settings import config
from utils.logger import get_logger
from utils.exception_handler import AppException
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser

logger = get_logger(__name__)


class PatchManager:
    """
    Class to manage patch generation, identification of special commits,
    and cleanup of patch files.

    Attributes:
        patches_dir (str): Directory where patches are stored temporarily.
        special_strings (List[str]): List of strings to identify special commits.
        special_patches (Dict[str, List[Dict]]): Dictionary to hold special commits for 'grpower' and 'nebula'.
    """

    def __init__(self):
        """
        Initialize the PatchManager with necessary configurations.
        """
        self.patches_dir = '/tmp/patches'  # Temporary directory for patch files
        self.special_strings = ['] thyp-sdk: ', '] nebula-sdk: ', '] tee: ']
        self.special_patches = {
            'grpower': [],
            'nebula': []
        }
        # Ensure the patches directory exists
        if not os.path.exists(self.patches_dir):
            os.makedirs(self.patches_dir)
            logger.info(f"Created temporary patches directory at {self.patches_dir}")

    def generate_patches(self, repository_configs: List):
        """
        Generate patch files for repositories between their latest and second latest tags.
        Special commits are handled separately.

        :param repository_configs: List of RepositoryConfig objects.
        """
        for repo_config in repository_configs:
            logger.info(f"Processing repository: {repo_config.name}")
            # Skip 'nebula' and 'grpower' repositories
            if repo_config.name in ['nebula', 'grpower']:
                logger.info(f"Skipping patch generation for repository: {repo_config.name}")
                continue

            # Handle repositories managed by 'repo' or 'jiri'
            if repo_config.repo_type in ['repo', 'jiri']:
                self._process_manifest_repo(repo_config)
            else:
                self._generate_repo_patches(repo_config)

    def _process_manifest_repo(self, repo_config):
        """
        Process repositories managed by 'repo' or 'jiri' tools.

        :param repo_config: RepositoryConfig object.
        """
        manifest_parser = ManifestParser(repo_config.manifest_path)
        projects = manifest_parser.get_projects()
        for project in projects:
            sub_repo_path = os.path.join(repo_config.path, project['path'])
            sub_repo_config = repo_config
            sub_repo_config.path = sub_repo_path
            self._generate_repo_patches(sub_repo_config)

    def _generate_repo_patches(self, repo_config):
        """
        Generate patches for a single repository.

        :param repo_config: RepositoryConfig object.
        """
        try:
            git_handler = GitHandler(repo_config.path)
            # Ensure tags are set
            if not repo_config.latest_tag or not repo_config.second_latest_tag:
                tags = git_handler.get_latest_tags(2)
                if len(tags) < 2:
                    logger.warning(f"Not enough tags found in {repo_config.name}")
                    return
                repo_config.latest_tag = tags[0]
                repo_config.second_latest_tag = tags[1]
            # Get commits between tags
            commits = git_handler.get_commits_between_tags(
                repo_config.second_latest_tag, repo_config.latest_tag)
            if not commits:
                logger.info(f"No new commits in {repo_config.name} between tags.")
                return
            # Identify special commits
            normal_commits = self._identify_special_commits(commits, repo_config)
            if not normal_commits:
                logger.info(f"No normal commits to generate patches for in {repo_config.name}")
                return
            # Generate patches using git format-patch
            patch_output_dir = os.path.join(self.patches_dir, repo_config.name)
            if not os.path.exists(patch_output_dir):
                os.makedirs(patch_output_dir)
            self._run_format_patch(repo_config.path, repo_config.second_latest_tag,
                                   repo_config.latest_tag, patch_output_dir)
            logger.info(f"Patches generated for repository {repo_config.name} at {patch_output_dir}")
        except AppException as e:
            logger.error(f"Error processing repository {repo_config.name}: {e}")

    def _identify_special_commits(self, commits: List[Dict], repo_config):
        """
        Identify special commits and assign them to 'grpower' or 'nebula' patches.

        :param commits: List of commit dictionaries.
        :param repo_config: RepositoryConfig object.
        :return: List of normal commits (excluding special commits).
        """
        normal_commits = []
        for commit in commits:
            message = commit['message']
            if any(special_str in message for special_str in self.special_strings):
                # Assign to grpower or nebula based on criteria
                if '] tee: ' in message:
                    self.special_patches['nebula'].append(commit)
                    logger.debug(f"Assigned commit {commit['commit_id']} to 'nebula' special patches")
                else:
                    self.special_patches['grpower'].append(commit)
                    logger.debug(f"Assigned commit {commit['commit_id']} to 'grpower' special patches")
            else:
                normal_commits.append(commit)
        return normal_commits

    def _run_format_patch(self, repo_path: str, older_tag: str, newer_tag: str, output_dir: str):
        """
        Run git format-patch command to generate patches.

        :param repo_path: Path to the Git repository.
        :param older_tag: The older tag name.
        :param newer_tag: The newer tag name.
        :param output_dir: Directory to save the patch files.
        :raises AppException: If the git command fails.
        """
        cmd = [
            'git', '-C', repo_path, 'format-patch',
            f'{older_tag}..{newer_tag}',
            '--output-directory', output_dir
        ]
        logger.debug(f"Running command: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Patch files generated in {output_dir}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running git format-patch: {e.stderr.decode().strip()}")
            raise AppException(f"Failed to generate patches in {repo_path}")

    def cleanup_patches(self):
        """
        Delete the temporary patches directory and all its contents.
        """
        if os.path.exists(self.patches_dir):
            shutil.rmtree(self.patches_dir)
            logger.info(f"Cleaned up patch files at {self.patches_dir}")
        else:
            logger.warning(f"Patches directory does not exist: {self.patches_dir}")

    def get_special_patches(self) -> Dict[str, List[Dict]]:
        """
        Get the special patches assigned to 'grpower' and 'nebula'.

        :return: Dictionary with keys 'grpower' and 'nebula' containing lists of commits.
        """
        return self.special_patches

    # Additional methods can be implemented as needed

# Example usage (to be removed or placed in a separate script)

# Initialize the PatchManager
# patch_manager = PatchManager()

# Generate patches for the repositories
# patch_manager.generate_patches(config.repositories)

# After processing is complete, clean up the patches
# patch_manager.cleanup_patches()