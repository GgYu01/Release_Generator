import subprocess
from typing import List, Dict
from pathlib import Path
from core.git_handler import GitHandler

class PatchManager:
    def __init__(self, repo_path: str, old_tag: str, new_tag: str) -> None:
        self.git_handler = GitHandler(repo_path)
        self.old_tag = old_tag
        self.new_tag = new_tag

    def generate_patches(self, output_dir: str) -> List[Path]:
        cmd = [
            'git', 'format-patch', f'{self.old_tag}...{self.new_tag}', 
            '--output-directory', output_dir
        ]
        subprocess.run(cmd, cwd=self.git_handler.repo_path)
        patch_files = list(Path(output_dir).glob('*.patch'))
        return patch_files

    @staticmethod
    def extract_commit_id_from_patch(patch_file_path: Path) -> str:
        with patch_file_path.open('r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('From '):
                    parts = line.strip().split(' ')
                    if len(parts) > 1:
                        return parts[1]
        return ''
