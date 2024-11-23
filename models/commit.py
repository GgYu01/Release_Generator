from dataclasses import dataclass
from typing import Optional

@dataclass
class Commit:
    id: str
    message: str
    author: str
    date: str
    patch_path: Optional[str] = None