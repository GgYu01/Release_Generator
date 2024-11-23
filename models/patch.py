from dataclasses import dataclass

@dataclass
class Patch:
    file_path: str
    commit_id: str
    repository: str