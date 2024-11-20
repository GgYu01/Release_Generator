#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for the Release Note Generator script.
"""

import sys
from config.settings import Settings
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser
from core.commit_processor import CommitProcessor
from core.patch_manager import PatchManager
from core.release_note_writer import ReleaseNoteWriter
from utils.logger import logger
from tasks.task_executor import TaskExecutor

def main():
    try:
        settings = Settings()
        logger.info("Initialized settings")

        git_handler = GitHandler(settings)
        logger.info("Initialized GitHandler")

        manifest_parser = ManifestParser(settings)
        logger.info("Initialized ManifestParser")

        commit_processor = CommitProcessor(settings, git_handler, manifest_parser)
        logger.info("Initialized CommitProcessor")

        patch_manager = PatchManager(settings, git_handler, manifest_parser)
        logger.info("Initialized PatchManager")

        release_note_writer = ReleaseNoteWriter(settings, git_handler)
        logger.info("Initialized ReleaseNoteWriter")

        # Initialize task executor
        task_executor = TaskExecutor(settings, git_handler, manifest_parser, commit_processor, patch_manager, release_note_writer)
        logger.info("Initialized TaskExecutor")

        task_executor.execute()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
