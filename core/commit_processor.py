# core/commit_processor.py
"""
Commit information processing module to parse updates between two tags.
"""

from typing import List, Dict
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class CommitProcessor:
    """
    Processes commit information between two tags.
    """

    def __init__(self):
        self.special_keywords = settings.SPECIAL_COMMIT_KEYWORDS

    def filter_special_commits(self, commits: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Filters commits containing special keywords.

        :param commits: List of commit dictionaries.
        :return: Filtered list of commits.
        """
        filtered_commits = []
        for commit in commits:
            if any(keyword in commit['message'] for keyword in self.special_keywords):
                filtered_commits.append(commit)
        logger.info(f"Filtered {len(filtered_commits)} special commits")
        return filtered_commits
