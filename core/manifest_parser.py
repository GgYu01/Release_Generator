# core/manifest_parser.py

import os
import xml.etree.ElementTree as ET
from typing import List, Dict
from utils.logger import get_logger
from utils.exception_handler import ManifestException

logger = get_logger(__name__)


class ManifestParser:
    """
    Class to parse manifest XML files and extract project information.

    Attributes:
        manifest_path (str): Path to the manifest XML file.
        root (Element): Root element of the parsed XML tree.
    """

    def __init__(self, manifest_path: str):
        """
        Initialize the ManifestParser with the manifest file path.

        :param manifest_path: Absolute path to the manifest XML file.
        :raises ManifestException: If the file does not exist or cannot be parsed.
        """
        self.manifest_path = manifest_path
        if not os.path.exists(manifest_path):
            logger.error(f"Manifest file does not exist: {manifest_path}")
            raise ManifestException(f"Manifest file does not exist: {manifest_path}")
        try:
            tree = ET.parse(manifest_path)
            self.root = tree.getroot()
            logger.info(f"Parsed manifest file: {manifest_path}")
        except ET.ParseError as e:
            logger.error(f"Error parsing manifest file: {e}")
            raise ManifestException(f"Error parsing manifest file: {e}") from e

    def get_projects(self) -> List[Dict]:
        """
        Extract project information from the manifest file.

        :return: List of dictionaries containing project details.
        :raises ManifestException: If unable to extract project information.
        """
        try:
            projects = []
            for project in self.root.findall('project'):
                name = project.get('name')
                path = project.get('path') or name
                remote = project.get('remote')
                revision = project.get('revision')
                project_info = {
                    'name': name,
                    'path': path,
                    'remote': remote,
                    'revision': revision,
                }
                projects.append(project_info)
            logger.debug(f"Extracted {len(projects)} projects from manifest")
            return projects
        except Exception as e:
            logger.error(f"Error extracting projects from manifest: {e}")
            raise ManifestException(f"Error extracting projects: {e}") from e

    # Additional methods for manifest parsing can be added here