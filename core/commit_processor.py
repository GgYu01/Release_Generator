from typing import List
from core.git_handler import GitHandler

class CommitProcessor:
    def __init__(self, repo_path: str, old_tag: str, new_tag: str) -> None:
        self.git_handler = GitHandler(repo_path)
        self.old_tag = old_tag
        self.new_tag = new_tag

    def process_commits(self) -> List[str]:
        commits = self.git_handler.get_commit_logs_between_tags(self.old_tag, self.new_tag)
        return commits