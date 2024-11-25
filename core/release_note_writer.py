from typing import List
from pathlib import Path

class ReleaseNoteWriter:
    def __init__(self, output_path: str) -> None:
        self.output_path = Path(output_path)

    def write(self, content: str) -> None:
        with self.output_path.open('w', encoding='utf-8') as f:
            f.write(content)