# core/release_note_generator.py
"""
Module to generate release notes.
"""

from core.git_handler import GitHandler
from core.commit_processor import CommitProcessor
from core.release_note_writer import ReleaseNoteWriter
from core.patch_manager import PatchManager
from utils.logger import get_logger
from config import settings
import subprocess

logger = get_logger(__name__)

def generate_release_notes():
    """
    生成发布说明，处理所有仓库的提交信息。
    """
    try:
        git_handler = GitHandler()
        commit_processor = CommitProcessor()
        patch_manager = PatchManager()
        release_note_writer = ReleaseNoteWriter("Release_Note.xlsx")

        # 获取日期标识
        date_identifiers = git_handler.get_date_identifiers_from_grt()
        if not date_identifiers:
            logger.error("Failed to retrieve date identifiers from GRT repository.")
            return
        old_date_id, new_date_id = date_identifiers[1], date_identifiers[0]

        # 构建所有仓库的 TAG
        repo_tags = git_handler.construct_tags_for_repositories(date_identifiers)

        # 获取所有仓库，包括子仓库
        repositories_to_process = git_handler.get_all_repositories()

        for repo_info in repositories_to_process:
            repo_name = repo_info['name']
            repo_path = repo_info['path']
            tool = repo_info.get('tool', 'git')
            tags = repo_tags.get(repo_name, {})
            old_tag = tags.get('old_tag')
            new_tag = tags.get('new_tag')

            if not old_tag or not new_tag:
                logger.error(f"No tags found for repository {repo_name}")
                continue

            logger.info(f"Processing repository: {repo_name}")

            commits = git_handler.get_commits_between_tags(repo_path, old_tag, new_tag, tool)
            if not commits:
                logger.info(f"No commits found between {old_tag} and {new_tag} in {repo_name}")
                continue

            # 对除 nebula 和 grpower 外的仓库，生成 patches
            if repo_name not in ['nebula', 'grpower']:
                patches = patch_manager.generate_patches_between_tags(repo_path, old_tag, new_tag, tool)
                commit_processor.match_commits_with_patches(commits, patches)

            # 处理特殊的 commits
            if repo_path in [settings.GRT_PATH, settings.ALPS_GRTPATH]:
                special_commits = commit_processor.filter_special_commits(commits, repo_name, repo_path)
                commit_processor.assign_special_commits_to_nebula_grpower(special_commits)

            # 准备数据写入发布说明
            for commit in commits:
                commit['release_version'] = new_tag
                commit['module'] = commit_processor.get_module_name(commit, repo_name, repo_path)
                commit['patch_paths'] = commit.get('patch_path', '')
                commit['submission_info'] = commit_processor.get_submission_info()
                # 其他字段根据需求设置

            release_note_writer.insert_commits(commits)

        release_note_writer.save()
        patch_manager.cleanup_patches()

    except Exception as e:
        logger.error(f"An error occurred: {e}")