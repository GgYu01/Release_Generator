from typing import List
from core.git_handler import GitHandler
from pathlib import Path

class PatchManager:
    def __init__(self, repo_path: str, old_tag: str, new_tag: str) -> None:
        self.git_handler = GitHandler(repo_path)
        self.old_tag = old_tag
        self.new_tag = new_tag

    def generate_patches(self, output_dir: str) -> List[Path]:
        cmd = ['git', 'format-patch', f'{self.old_tag}..{self.new_tag}', '-o', output_dir]
        subprocess.run(cmd, cwd=self.git_handler.repo_path)
        patches = list(Path(output_dir).glob('*.patch'))
        return patches