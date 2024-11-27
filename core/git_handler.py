import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class GitHandler:
    def __init__(self, repo_path: str) -> None:
        self.repo_path = Path(repo_path)

    def get_last_two_tags(self) -> Tuple[str, str]:
        cmd = ['git', 'tag', '--sort=-creatordate']
        result = subprocess.run(cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True)
        tags = result.stdout.strip().split('\n')
        return (tags[0], tags[1]) if len(tags) >= 2 else (tags[0], None)

    def get_commit_logs_between_tags(self, old_tag: str, new_tag: str) -> List[Dict[str, str]]:
        cmd = [
            'git', 'log', f'{old_tag}...{new_tag}',
            '--format=%H%x01%B%x02', '--no-merges'
        ]
        result = subprocess.run(
            cmd, cwd=self.repo_path, stdout=subprocess.PIPE, text=True
        )
        logs = []
        entries = result.stdout.strip().split('\x02\n')
        for entry in entries:
            if entry:
                parts = entry.strip().split('\x01', 1)
                if len(parts) == 2:
                    commit_id = parts[0]
                    message = parts[1].strip()
                    logs.append({'commit_id': commit_id, 'message': message})
        return logs

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