# -*- coding: utf-8 -*-

"""
Module for executing tasks related to the release note generation.
"""

from utils.logger import logger
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser
from core.commit_processor import CommitProcessor
from core.patch_manager import PatchManager
from core.release_note_writer import ReleaseNoteWriter
from utils.exception_handler import GitOperationException
import openpyxl
import os

class TaskExecutor:
    def __init__(self, settings, git_handler: GitHandler, manifest_parser: ManifestParser, commit_processor: CommitProcessor, patch_manager: PatchManager, release_note_writer: ReleaseNoteWriter):
        self.settings = settings
        self.git_handler = git_handler
        self.manifest_parser = manifest_parser
        self.commit_processor = commit_processor
        self.patch_manager = patch_manager
        self.release_note_writer = release_note_writer

    def execute(self):
        """
        Execute the task of generating release notes.
        """
        logger.info("Starting task execution")

        # Parse all repositories
        repositories = self.manifest_parser.get_all_repositories()

        # Construct tags for all repositories based on their own tag patterns
        constructed_tags = {}
        for repo_name, repo_path in repositories:
            try:
                latest_tag, second_latest_tag = self.git_handler.get_latest_tags_for_repo(repo_path)
                constructed_tag = self.git_handler.construct_tag_for_repo(latest_tag, repo_path)
                constructed_second_tag = self.git_handler.construct_tag_for_repo(second_latest_tag, repo_path)
                constructed_tags[repo_path] = (constructed_tag, constructed_second_tag)
                logger.debug(f"Constructed tags for {repo_path}: {constructed_tag}, {constructed_second_tag}")
            except GitOperationException as e:
                logger.error(f"Skipping repository {repo_path} due to tag retrieval error: {e}")
                continue

        # Get all commits info with per-repo tags
        commits_info = self.commit_processor.get_all_commits_info(repositories, constructed_tags)

        # Generate patches and associate them with commits
        patch_mapping = self.patch_manager.generate_and_associate_patches(repositories, constructed_tags, commits_info)

        # Update release notes
        self.release_note_writer.update_release_note(commits_info, constructed_tags, patch_mapping)

        # Clean up patches
        self.patch_manager.clean_patches(repositories)

        logger.info("Task execution completed successfully")
