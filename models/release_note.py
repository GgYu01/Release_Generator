from dataclasses import dataclass
from typing import List

@dataclass
class ReleaseNoteEntry:
    release_version: str
    functionality: str
    module: str
    patch_file: str
    example_code_path: str
    commit_info: str
    test_leader: str
    commit_id: str

@dataclass
class ReleaseNote:
    entries: List[ReleaseNoteEntry]