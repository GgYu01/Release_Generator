# config/settings.py

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class RepositoryConfig:
    """Data class to store repository configuration."""
    name: str                  # Repository name, e.g., 'grpower', 'grt'
    path: str                  # Absolute path to the repository
    repo_type: str             # Type of repository: 'git', 'repo', 'jiri'
    manifest_path: str = ''    # Path to the manifest file, if applicable
    latest_tag: str = ''       # Latest Git tag
    second_latest_tag: str = ''  # Second latest Git tag


@dataclass
class Config:
    """Main configuration data class."""
    # List of repository configurations
    repositories: List[RepositoryConfig] = field(default_factory=list)
    
    # Logging configuration
    log_level: str = 'INFO'
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Other configurations can be added here
    # e.g., default values, API configurations, etc.

    # Example default values for Release Note columns
    default_test_leader: str = 'Test Leader Name'
    default_modifier: str = 'Modifier Name'
    default_mtk_owner: str = 'MTK Owner Name'


# Initialize the configuration with repository details
config = Config(
    repositories=[
        RepositoryConfig(
            name='grpower',
            path='/home/nebula/grpower',
            repo_type='git'
        ),
        RepositoryConfig(
            name='grt',
            path='/home/nebula/grt',
            repo_type='git'
        ),
        RepositoryConfig(
            name='grt_be',
            path='/home/nebula/grt_be',
            repo_type='git'
        ),
        RepositoryConfig(
            name='alps',
            path='/home/nebula/alps',
            repo_type='repo',
            manifest_path='/home/nebula/alps/.repo/manifests/mt8678/grt/1001/alps.xml'
        ),
        RepositoryConfig(
            name='yocto',
            path='/home/nebula/yocto',
            repo_type='repo',
            manifest_path='/home/nebula/yocto/.repo/manifests/mt8678/grt/1001/yocto.xml'
        ),
        RepositoryConfig(
            name='nebula',
            path='/home/nebula/grpower/workspace/nebula',
            repo_type='jiri',
            manifest_path='/home/nebula/grpower/workspace/nebula/manifest/cci/nebula-main'
        ),
    ]
)