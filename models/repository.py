from dataclasses import dataclass
from typing import List

@dataclass
class Repository:
    name: str
    path: str
    manager: str
    tags: List[str]
    commits: List['Commit']
    patches: List['Patch']