# -*- coding: utf-8 -*-

"""
Module for parsing manifest files to extract repository information.
"""

import os
import xml.etree.ElementTree as ET
from utils.logger import logger
from utils.exception_handler import ManifestParseException
from typing import List, Tuple

class ManifestParser:
    def __init__(self, settings):
        self.settings = settings

    def parse_manifest(self, manifest_path: str) -> List[str]:
        """
        Parse a manifest XML file to get repository paths.
        """
        try:
            full_path = os.path.abspath(manifest_path)
            if not os.path.exists(full_path):
                logger.error(f"Manifest file does not exist: {full_path}")
                return []
            tree = ET.parse(full_path)
            root = tree.getroot()
            repo_list = []
            for project in root.findall('.//project'):
                repo_path = project.get('path')
                if repo_path:
                    repo_list.append(repo_path)
            logger.info(f"Parsed {len(repo_list)} repositories from {manifest_path}")
            return repo_list
        except Exception as e:
            logger.error(f"Failed to parse manifest {manifest_path}: {e}")
            raise ManifestParseException(f"Failed to parse manifest {manifest_path}")

    def get_all_repositories(self) -> List[Tuple[str, str]]:
        """
        Get all repositories and their absolute paths from manifests.
        Returns a list of tuples containing (repository name, absolute path).
        """
        repositories = []

        # Parse nebula manifest
        nebula_manifest_path = os.path.join(self.settings.nebula_path, self.settings.nebula_manifest)
        nebula_repos = self.parse_manifest(nebula_manifest_path)
        repositories.extend([(repo, os.path.join(self.settings.nebula_path, repo)) for repo in nebula_repos])

        # Parse alps manifest
        alps_manifest_path = os.path.join(self.settings.alps_path, self.settings.alps_manifest)
        alps_repos = self.parse_manifest(alps_manifest_path)
        repositories.extend([(repo, os.path.join(self.settings.alps_path, repo)) for repo in alps_repos])

        # Parse yocto manifest
        yocto_manifest_path = os.path.join(self.settings.yocto_path, self.settings.yocto_manifest)
        yocto_repos = self.parse_manifest(yocto_manifest_path)
        repositories.extend([(repo, os.path.join(self.settings.yocto_path, repo)) for repo in yocto_repos])

        # Add main repositories
        main_repos = [
            ('grpower', self.settings.grpower_path),
            ('grt', self.settings.grt_path),
            ('grt_be', self.settings.grt_be_path),
            ('yocto', self.settings.yocto_path),
            ('alps', self.settings.alps_path),
            ('nebula', self.settings.nebula_path),
        ]
        repositories.extend(main_repos)

        # Remove duplicates
        unique_repos = list({repo[1]: repo for repo in repositories}.values())
        logger.info(f"Total repositories to process: {len(unique_repos)}")
        return unique_repos
