import os
from typing import List

def list_files(directory: str, extension: str = "") -> List[str]:
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    with open(file_path, 'w') as file:
        file.write(content)

def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)