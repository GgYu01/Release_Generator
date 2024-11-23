import os
from typing import Any, Dict

def merge_dicts(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    merged = dict1.copy()
    merged.update(dict2)
    return merged

def sanitize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))