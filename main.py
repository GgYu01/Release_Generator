from core.commit_processor import CommitProcessor
from core.patch_manager import PatchManager
from core.release_note_writer import ReleaseNoteWriter

def main():
    commit_processor = CommitProcessor()
    commits = commit_processor.process_commits()

    patch_manager = PatchManager(commits)
    patch_manager.generate_patches()

    release_note_writer = ReleaseNoteWriter(commits)
    release_note_writer.write_release_notes()

    patch_manager.cleanup_patches()

if __name__ == "__main__":
    main()
