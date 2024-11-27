from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class CommitInfo:
    commit_id: str
    message: str
    patch_file: Optional[str] = None  # Add patch file path

@dataclass
class RepositoryInfo:
    name: str
    path: str
    parent: Optional[str]
    latest_tag: str
    previous_tag: str
    commits: List[CommitInfo] = field(default_factory=list)  # Updated to use CommitInfo

@dataclass
class RepositoryConfig:
    name: str
    path: str
    manifest: str
    tag_prefix: str
    remote: str = ''
    remotebranch: str = ''

@dataclass
class Settings:
    repositories: List[RepositoryConfig] = field(default_factory=list)
    api_settings: Dict[str, Any] = field(default_factory=dict)
    log_level: str = 'DEBUG'  # Added log level configuration
    log_file: str = 'release_note_generator.log'  # Added log file configuration

    def __post_init__(self):
        self.repositories = [
            RepositoryConfig(
                name='nebula',
                path='/home/nebula/grpower/workspace/nebula',
                manifest='/home/nebula/grpower/workspace/nebula/manifest/cci/nebula-main',
                tag_prefix='release-spm.mt8678_mt8676_'
            ),
            RepositoryConfig(
                name='alps',
                path='/home/nebula/alps',
                manifest='/home/nebula/alps/.repo/manifests/mt8678/grt/1114/alps.xml',
                tag_prefix='release-spm.mt8678_'
            ),
            RepositoryConfig(
                name='yocto',
                path='/home/nebula/yocto',
                manifest='/home/nebula/yocto/.repo/manifests/mt8678/grt/1114/yocto.xml',
                tag_prefix='release-spm.mt8678_'
            ),
            RepositoryConfig(
                name='grpower',
                path='/home/nebula/grpower',
                manifest='',
                tag_prefix='release-spm.mt8678_'
            ),
            RepositoryConfig(
                name='grt',
                path='/home/nebula/grt',
                manifest='',
                tag_prefix='release-spm.mt8678_'
            ),
            RepositoryConfig(
                name='grt_be',
                path='/home/nebula/grt_be',
                manifest='',
                tag_prefix='release-spm.mt8678_'
            ),
        ]
        self.api_settings = {
            'host': '0.0.0.0',
            'port': 8000,
            'debug': True
        }
        # Set log level and log file path as needed
        self.log_level = 'DEBUG'
        self.log_file = '/home/nebula/Release_Generator/logfile.log'

settings = Settings()
