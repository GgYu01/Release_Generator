from typing import List, Tuple
import subprocess
from pathlib import Path

class GitHandler:
    def __init__(self, repo_path: str) -> None:
        self.repo_path = Path(repo_path)

    def get_last_two_tags(self) -> Tuple[str, str]:
        cmd = ['git', 'tag', '--sort=-creatordate']
        result = subprocess.run(cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True)
        tags = result.stdout.strip().split('\n')
        return (tags[0], tags[1]) if len(tags) >= 2 else (tags[0], None)

    def get_commit_logs_between_tags(self, old_tag: str, new_tag: str) -> List[str]:
        cmd = ['git', 'log', f'{old_tag}...{new_tag}', '--oneline']
        result = subprocess.run(cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True)
        return result.stdout.strip().split('\n')

    def fetch_tags(self) -> None:
        cmd = ['git', 'fetch', '--tags']
        subprocess.run(cmd, cwd=self.repo_path)

    def get_submodule_paths(self) -> List[str]:
        cmd = ['git', 'submodule', 'foreach', '--quiet', 'echo $path']
        result = subprocess.run(cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True, shell=True)
        return result.stdout.strip().split('\n')

    def get_all_tags(self) -> List[str]:
        cmd = ['git', 'tag']
        result = subprocess.run(cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True)
        tags = result.stdout.strip().split('\n')
        return tags