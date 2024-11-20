# core/manifest_parser.py
"""
Manifest file parsing module to obtain repository list and paths.
"""

import os
from typing import List, Dict
import xml.etree.ElementTree as ET
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ManifestParser:
    """
    Parses manifest files to extract repository information.
    """

    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path

    def parse(self) -> List[Dict[str, str]]:
        """
        Parses the manifest file.

        :return: List of repositories with their paths.
        """
        try:
            tree = ET.parse(self.manifest_path)
            root = tree.getroot()
            repos = []
            for child in root:
                if child.tag == 'project':
                    name = child.attrib.get('name')
                    path = child.attrib.get('path', name)
                    repos.append({"name": name, "path": path})
            logger.info(f"Parsed {len(repos)} repositories from {self.manifest_path}")
            return repos
        except ET.ParseError as e:
            logger.error(f"Error parsing manifest file {self.manifest_path}: {e}")
            return []
        except FileNotFoundError:
            logger.error(f"Manifest file not found: {self.manifest_path}")
            return []
