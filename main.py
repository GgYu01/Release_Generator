# main.py
"""
Script entry point.
"""

from core.git_handler import GitHandler
from core.commit_processor import CommitProcessor
from core.release_note_writer import ReleaseNoteWriter
from core.patch_manager import PatchManager
from utils.logger import get_logger
from config import settings

logger = get_logger(__name__)


def main():
    """
    Main function to execute the release note generation process.
    """
    try:
        git_handler = GitHandler()
        commit_processor = CommitProcessor()
        patch_manager = PatchManager()
        release_note_writer = ReleaseNoteWriter("Release_Note.xlsx")

        # Example flow for a single repository
        grt_tags = git_handler.get_latest_tags(settings.GRT_PATH)
        if len(grt_tags) < 2:
            logger.error("Not enough tags found in GRT repository.")
            return

        old_tag, new_tag = grt_tags[1], grt_tags[0]
        commits = git_handler.get_commits_between_tags(settings.GRT_PATH, old_tag, new_tag)
        filtered_commits = commit_processor.filter_special_commits(commits)

        # Generate patches
        patches = patch_manager.generate_patches_for_repo(settings.GRT_PATH, old_tag, new_tag)

        # Prepare data for release note
        for commit in filtered_commits:
            commit['release_version'] = new_tag
            commit['module'] = 'thyp-sdk'
            commit['patch_paths'] = '\n'.join(patches)
            commit['submission_info'] = f"zircon: [commit_id]\ngarnet: [commit_id]"

        # Insert commits into the release note
        release_note_writer.insert_commits(filtered_commits)
        release_note_writer.save()

        # Clean up patches
        patch_manager.cleanup_patches()

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
