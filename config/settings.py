# -*- coding: utf-8 -*-

"""
Settings module containing all configuration parameters.
"""

import os
from dataclasses import dataclass, field

@dataclass
class Settings:
    # General Paths
    grpower_path: str = os.path.expanduser('~/grpower')
    grt_path: str = os.path.expanduser('~/grt')
    grt_be_path: str = os.path.expanduser('~/grt_be')
    nebula_path: str = os.path.expanduser('~/grpower/workspace/nebula')
    alps_path: str = os.path.expanduser('~/alps')
    yocto_path: str = os.path.expanduser('~/yocto')

    # Manifest Paths
    nebula_manifest: str = 'manifest/cci/nebula-main'
    alps_manifest: str = '.repo/manifests/mt8678/grt/1001/alps.xml'
    yocto_manifest: str = '.repo/manifests/mt8678/grt/1001/yocto.xml'

    # FastAPI Configuration
    api_host: str = '100.64.0.5'
    api_port: int = 4151

    # Default Values for Release Note Columns
    tester: str = '高宇轩'
    modifier: str = '武阳'
    mtk_owner: str = '金春阳'
    submission_time: str = '2024-11-20'
    porting_required: str = 'No'
    porting_status: str = 'N/A'
    release_customer: str = ''
    change_id: str = ''
    mtk_merge_date: str = ''
    mtk_registration_status: str = ''

    # Logger Configuration
    log_file: str = 'release_note_generator.log'
    log_level: str = 'DEBUG'

    # Commit Message Filters
    special_commit_filters: list = field(default_factory=lambda: [
        '] thyp-sdk: ',
        '] nebula-sdk: ',
        '] tee: '
    ])

    # Repository Paths for Column F
    zircon_repo: str = os.path.expanduser('~/grpower/workspace/nebula/zircon')
    garnet_repo: str = os.path.expanduser('~/grpower/workspace/nebula/garnet')

    def __post_init__(self):
        # Ensure all paths are absolute
        for attr in ['grpower_path', 'grt_path', 'grt_be_path', 'nebula_path', 'alps_path', 'yocto_path', 'zircon_repo', 'garnet_repo']:
            path = getattr(self, attr)
            if not os.path.isabs(path):
                setattr(self, attr, os.path.abspath(path))
