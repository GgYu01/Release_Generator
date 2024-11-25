from pathlib import Path
from typing import List

def list_files(directory: str) -> List[Path]:
    return list(Path(directory).glob('*'))

def read_file(file_path: str) -> str:
    return Path(file_path).read_text()

def write_file(file_path: str, content: str) -> None:
    Path(file_path).write_text(content)