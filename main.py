from typing import List, Dict, Optional, Set
from config.settings import settings, RepositoryInfo, CommitInfo
from core.manifest_parser import ManifestParser
from core.git_handler import GitHandler
from core.patch_manager import PatchManager
from utils.logger import get_logger
from utils.common import normalize_tag
from rich.console import Console
from rich.traceback import install
import os
from pathlib import Path

def main() -> None:
    install()  # Enable rich traceback
    console = Console()
    logger = get_logger('Main')

    console.log("[bold green]Starting Release Note Generator[/bold green]")
    logger.info("Starting Release Note Generator")

    # Get grt repository information
    grt_repo_config = next((repo for repo in settings.repositories if repo.name == 'grt'), None)
    if grt_repo_config is None:
        console.log("[red]grt repository not found in settings[/red]")
        logger.error("grt repository not found in settings")
        return

    grt_git_handler = GitHandler(grt_repo_config.path)
    grt_latest_tag, grt_previous_tag = grt_git_handler.get_last_two_tags()
    grt_tag_prefix = grt_repo_config.tag_prefix

    # Normalize tags to get version numbers
    grt_latest_version = normalize_tag(grt_latest_tag, grt_tag_prefix)
    grt_previous_version = normalize_tag(grt_previous_tag, grt_tag_prefix) if grt_previous_tag else None
    # grt_latest_version = "2024_1125_01"
    # grt_previous_version = "2024_1122_01"

    console.log(f"grt Latest version: {grt_latest_version}")
    logger.info(f"grt Latest version: {grt_latest_version}")
    console.log(f"grt Previous version: {grt_previous_version}")
    logger.info(f"grt Previous version: {grt_previous_version}")

    # Initialize list to store repositories with commits
    all_repositories_with_commits: List[RepositoryInfo] = []

    # For each repository in settings
    for repo_config in settings.repositories:
        repo_path = repo_config.path
        tag_prefix = repo_config.tag_prefix

        # Construct expected tags
        latest_tag = tag_prefix + grt_latest_version
        previous_tag = tag_prefix + grt_previous_version if grt_previous_version else ''

        console.log(f"[cyan]Processing repository: {repo_config.name}[/cyan]")
        logger.info(f"Processing repository: {repo_config.name}")

        git_handler = GitHandler(repo_path)

        # Get all tags in the repository
        tags = git_handler.get_all_tags()

        latest_tag_exists = latest_tag in tags
        previous_tag_exists = previous_tag in tags if previous_tag else False

        console.log(f"Expected latest tag: {latest_tag}, Exists: {latest_tag_exists}")
        logger.info(f"Expected latest tag: {latest_tag}, Exists: {latest_tag_exists}")

        if not latest_tag_exists:
            console.log(f"[red]Latest tag {latest_tag} does not exist in {repo_config.name}[/red]")
            logger.warning(f"Latest tag {latest_tag} does not exist in {repo_config.name}")

        if previous_tag and not previous_tag_exists:
            console.log(f"[red]Previous tag {previous_tag} does not exist in {repo_config.name}[/red]")
            logger.warning(f"Previous tag {previous_tag} does not exist in {repo_config.name}")

        # Initialize repository info data structure
        repo_info = RepositoryInfo(
            name=repo_config.name,
            path=repo_path,
            parent=None,
            latest_tag=latest_tag,
            previous_tag=previous_tag,
            commits=[]
        )

        # Determine whether to generate patches for this repository
        generate_patches = repo_config.name not in ['grpower', 'nebula']

        # Generate patches and get commits
        if latest_tag_exists and previous_tag_exists:
            commits = git_handler.get_commit_logs_between_tags(previous_tag, latest_tag)
            if commits:
                if generate_patches:
                    patch_manager = PatchManager(repo_path, previous_tag, latest_tag)
                    patch_files = patch_manager.generate_patches(repo_path)

                    # Map commits to patches
                    commit_patch_map: Dict[str, str] = {}
                    for patch_file in patch_files:
                        commit_id = patch_manager.extract_commit_id_from_patch(patch_file)
                        if commit_id:
                            relative_patch_path = os.path.relpath(str(patch_file), repo_path)
                            commit_patch_map[commit_id] = relative_patch_path

                    # Update commits with patch file paths
                    commit_infos: List[CommitInfo] = []
                    for commit in commits:
                        patch_file = commit_patch_map.get(commit['commit_id'])
                        commit_info = CommitInfo(
                            commit_id=commit['commit_id'],
                            message=commit['message'],
                            patch_file=patch_file
                        )
                        commit_infos.append(commit_info)
                        logger.debug(f"Commit ID: {commit['commit_id']} mapped to Patch File: {patch_file}")

                else:
                    # Do not generate patches, keep patch_file as None
                    commit_infos = [
                        CommitInfo(
                            commit_id=commit['commit_id'],
                            message=commit['message'],
                            patch_file=None
                        ) for commit in commits
                    ]

                # Update repository info
                repo_info.commits = commit_infos
                # Add to the list
                all_repositories_with_commits.append(repo_info)
                logger.info(f"Added {len(commit_infos)} commits for repository {repo_config.name}")

        # Process submodules if manifest exists
        if repo_config.manifest:
            manifest_parser = ManifestParser(repo_config)
            projects = manifest_parser.parse()
            console.log(f"Found {len(projects)} projects in manifest of {repo_config.name}")
            logger.info(f"Parsed {len(projects)} projects in manifest for {repo_config.name}")
            for project in projects:
                project_name = project['name']
                project_path = project['absolute_path']
                console.log(f"Processing project: {project_name} at {project_path}")
                logger.info(f"Processing project: {project_name} at {project_path}")

                project_git_handler = GitHandler(project_path)

                # Construct expected tags for the project
                project_latest_tag = tag_prefix + grt_latest_version
                project_previous_tag = tag_prefix + grt_previous_version if grt_previous_version else ''

                # Get all tags in the project repository
                project_tags = project_git_handler.get_all_tags()

                project_latest_tag_exists = project_latest_tag in project_tags
                project_previous_tag_exists = project_previous_tag in project_tags if project_previous_tag else False

                console.log(f"Expected latest tag: {project_latest_tag}, Exists: {project_latest_tag_exists}")
                logger.info(f"Expected latest tag: {project_latest_tag}, Exists: {project_latest_tag_exists}")

                if not project_latest_tag_exists:
                    console.log(f"[red]Latest tag {project_latest_tag} does not exist in {project_path}[/red]")
                    logger.warning(f"Latest tag {project_latest_tag} does not exist in {project_path}")

                if project_previous_tag and not project_previous_tag_exists:
                    console.log(f"[red]Previous tag {project_previous_tag} does not exist in {project_path}[/red]")
                    logger.warning(f"Previous tag {project_previous_tag} does not exist in {project_path}")

                # Initialize sub-repository info data structure
                project_repo_info = RepositoryInfo(
                    name=project_name,
                    path=project_path,
                    parent=repo_config.name,
                    latest_tag=project_latest_tag,
                    previous_tag=project_previous_tag,
                    commits=[]
                )

                # Determine whether to generate patches for this project
                if repo_config.name == 'nebula' or project_name in ['grpower', 'nebula']:
                    # Do not generate patches for sub-repositories of 'nebula' or for 'grpower' and 'nebula' projects
                    project_generate_patches = False
                else:
                    # Generate patches for other projects
                    project_generate_patches = True

                # Get commits between tags for the project
                if project_latest_tag_exists and project_previous_tag_exists:
                    project_commits = project_git_handler.get_commit_logs_between_tags(project_previous_tag, project_latest_tag)
                    if project_commits:
                        if project_generate_patches:
                            # Proceed with generating patches
                            project_patch_manager = PatchManager(project_path, project_previous_tag, project_latest_tag)
                            project_patch_files = project_patch_manager.generate_patches(project_path)

                            # Map commits to patches
                            project_commit_patch_map: Dict[str, str] = {}
                            for patch_file in project_patch_files:
                                project_commit_id = project_patch_manager.extract_commit_id_from_patch(patch_file)
                                if project_commit_id:
                                    relative_patch_path = os.path.relpath(str(patch_file), project_path)
                                    project_commit_patch_map[project_commit_id] = relative_patch_path

                            # Update commits with patch file paths
                            project_commit_infos: List[CommitInfo] = []
                            for commit in project_commits:
                                patch_file = project_commit_patch_map.get(commit['commit_id'])
                                commit_info = CommitInfo(
                                    commit_id=commit['commit_id'],
                                    message=commit['message'],
                                    patch_file=patch_file
                                )
                                project_commit_infos.append(commit_info)
                                logger.debug(f"Commit ID: {commit['commit_id']} mapped to Patch File: {patch_file}")

                        else:
                            # Do not generate patches, keep patch_file as None
                            project_commit_infos = [
                                CommitInfo(
                                    commit_id=commit['commit_id'],
                                    message=commit['message'],
                                    patch_file=None
                                ) for commit in project_commits
                            ]

                        # Update project repository info
                        project_repo_info.commits = project_commit_infos
                        # Add to the list
                        all_repositories_with_commits.append(project_repo_info)
                        logger.info(f"Added {len(project_commit_infos)} commits for project {project_name}")

        else:
            console.log(f"No manifest found for {repo_config.name}")
            logger.warning(f"No manifest found for {repo_config.name}")

    # Output the repositories with commits in order
    for repo_info in all_repositories_with_commits:
        parent_info = f"Parent Repository: {repo_info.parent}" if repo_info.parent else "Parent Repository: None"
        console.log(f"{parent_info} - Repository: {repo_info.name}")
        logger.info(f"Output commits for repository: {repo_info.name}")
        for commit in repo_info.commits:
            console.log(f"Commit ID: {commit.commit_id}")
            console.log(f"Commit Message:\n{commit.message}")
            console.log(f"Patch File: {commit.patch_file if commit.patch_file else 'None'}\n")
            logger.debug(f"Commit ID: {commit.commit_id}, Patch File: {commit.patch_file}")

    console.log("[bold green]Release Note Generation Completed[/bold green]")
    logger.info("Release Note Generation Completed")

if __name__ == "__main__":
    main()