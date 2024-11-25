from typing import List, Dict
import xml.etree.ElementTree as ET
from pathlib import Path
from config.settings import RepositoryConfig

class ManifestParser:
    def __init__(self, repo_config: RepositoryConfig) -> None:
        self.repo_config = repo_config
        self.manifest_path = Path(self.repo_config.manifest)

    def parse(self) -> List[Dict[str, str]]:
        tree = ET.parse(self.manifest_path)
        root = tree.getroot()
        projects = []
        repo_root_path = Path(self.repo_config.path)
        for project in root.iter('project'):
            name = project.get('name')
            path = project.get('path')
            remote = project.get('remote')
            remotebranch = project.get('remotebranch')
            # Resolve the absolute path of the repository
            absolute_path = (repo_root_path / path).resolve()
            projects.append({
                'name': name,
                'path': path,
                'absolute_path': str(absolute_path),
                'remote': remote,
                'remotebranch': remotebranch
            })
        return projects