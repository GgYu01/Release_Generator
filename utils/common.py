# utils/common.py

import re
from typing import List

def determine_parent_repos(commit_message: str) -> List[str]:
    patterns = {
        r'\] thyp-sdk: ': 'nebula-hyper',
        r'\] nebula-sdk: ': 'nebula-sdk',
        r'\] tee: ': 'TEE',
    }
    parents = []
    for pattern, parent in patterns.items():
        if re.search(pattern, commit_message):
            parents.append(parent)
    return parents

def normalize_tag(tag: str, prefix_to_remove: str) -> str:
    if tag.startswith(prefix_to_remove):
        return tag[len(prefix_to_remove):]
    return tag