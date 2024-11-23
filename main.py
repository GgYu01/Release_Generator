# main.py

import sys
import asyncio
from typing import List, Dict

# Import configuration and utilities
from config.settings import config
from utils.logger import get_logger
from utils.exception_handler import AppException

# Import core modules
from core.git_handler import GitHandler
from core.manifest_parser import ManifestParser
from core.commit_processor import CommitProcessor
from core.patch_manager import PatchManager
from core.release_note_writer import ReleaseNoteWriter

# Import task management
from tasks.task_queue import TaskQueue
from tasks.task_executor import TaskExecutor

# Initialize logger
logger = get_logger(__name__)


async def main():
    """
    Main function to initiate the Release Note generation process.
    """
    try:
        logger.info("Starting Release Note Generation Process")
        
        # Initialize task queue
        task_queue = TaskQueue()
        
        # Load repositories from configuration
        repositories = config.repositories
        
        # List to store all repository tasks
        tasks = []
        
        # Process each repository
        for repo_config in repositories:
            repo_task = asyncio.create_task(process_repository(repo_config))
            tasks.append(repo_task)
            logger.info(f"Initialized task for repository: {repo_config.name}")
        
        # Await all repository tasks
        await asyncio.gather(*tasks)
        
        # Once all tasks are completed, generate the Release Note
        release_note_writer = ReleaseNoteWriter()
        release_note_writer.write_release_notes()
        
        logger.info("Release Note Generation Process Completed Successfully")
    
    except AppException as e:
        logger.error(f"Application exception occurred: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


async def process_repository(repo_config):
    """
    Process a single repository: get tags, commits, and generate patches.

    :param repo_config: RepositoryConfig object with repository details.
    """
    try:
        logger.info(f"Processing repository: {repo_config.name}")
        
        # Initialize GitHandler
        git_handler = GitHandler(repo_config.path)
        
        # Get the latest and second latest tags
        tags = git_handler.get_latest_tags(n=2)
        if len(tags) < 2:
            logger.warning(f"Not enough tags in repository {repo_config.name}")
            return
        
        repo_config.latest_tag = tags[0]
        repo_config.second_latest_tag = tags[1]
        logger.info(f"Latest tags for {repo_config.name}: {tags}")
        
        # Get commits between the two tags
        commits = git_handler.get_commits_between_tags(
            older_tag=repo_config.second_latest_tag,
            newer_tag=repo_config.latest_tag
        )
        logger.info(f"Found {len(commits)} commits in {repo_config.name}")
        
        # Process manifest if applicable
        if repo_config.repo_type in ('repo', 'jiri'):
            manifest_parser = ManifestParser(repo_config.manifest_path)
            projects = manifest_parser.get_projects()
            logger.info(f"Parsed {len(projects)} projects from manifest in {repo_config.name}")
        else:
            projects = [{'name': repo_config.name, 'path': repo_config.path}]
        
        # Process commits and generate patches
        commit_processor = CommitProcessor(repo_config, commits, projects)
        commit_processor.process_commits()
        
        patch_manager = PatchManager(repo_config, commit_processor.commit_map)
        patch_manager.generate_patches()
        
        # Store processed data for Release Note Writer
        ReleaseNoteWriter.add_repository_data(repo_config.name, commit_processor.commit_map)
        
        logger.info(f"Completed processing for repository: {repo_config.name}")
    
    except AppException as e:
        logger.error(f"Error processing repository {repo_config.name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in repository {repo_config.name}: {e}")


if __name__ == "__main__":
    # Run the main function asynchronously
    asyncio.run(main())