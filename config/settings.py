# config/settings.py
"""
Global configuration settings.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Settings:
    """
    Configuration settings for the release note generator.
    """
    # Paths
    NEBULA_PATH: str = "/home/nebula/grpower/workspace/nebula/"
    GRPOWER_PATH: str = "/home/nebula/grpower/"
    GRT_PATH: str = "/home/nebula/grt/"
    GRT_BE_PATH: str = "/home/nebula/grt_be/"
    ALPS_PATH: str = "/home/nebula/alps/"
    YOCTO_PATH: str = "/home/nebula/yocto/"

    # Manifest files
    NEBULA_MANIFEST: str = "manifest/cci/nebula-main"
    ALPS_MANIFEST: str = ".repo/manifests/mt8678/grt/1001/alps.xml"
    YOCTO_MANIFEST: str = ".repo/manifests/mt8678/grt/1001/yocto.xml"

    # FastAPI settings
    API_HOST: str = "100.64.0.5"
    API_PORT: int = 4151

    # Default values for release note columns
    TEST_LEADER: str = "Test Leader"
    MODIFIER: str = "Modifier"
    MTK_OWNER: str = "MTK Owner"
    SUBMISSION_TIME: str = "2024-11-20"
    IS_PORTED: str = "No"
    IS_TESTED: str = "No"
    CUSTOMER_RELEASE: str = ""
    CHANGE_ID: str = ""
    MTK_MERGE_DATE: str = ""
    MTK_REGISTRATION_STATUS: str = ""

    # Repositories configuration
    REPOSITORIES: List[Dict[str, str]] = field(default_factory=lambda: [
        {"name": "nebula", "tool": "jiri", "path": "/home/nebula/grpower/workspace/nebula/"},
        {"name": "grpower", "tool": "git", "path": "/home/nebula/grpower/"},
        {"name": "grt", "tool": "git", "path": "/home/nebula/grt/"},
        {"name": "grt_be", "tool": "git", "path": "/home/nebula/grt_be/"},
        {"name": "alps", "tool": "repo", "path": "/home/nebula/alps/"},
        {"name": "yocto", "tool": "repo", "path": "/home/nebula/yocto/"},
    ])

    # Commit keywords for special handling
    SPECIAL_COMMIT_KEYWORDS: List[str] = field(default_factory=lambda: [
        "] thyp-sdk: ",
        "] nebula-sdk: ",
        "] tee: ",
    ])

    # Paths for zircon and garnet
    ZIRCON_PATH: str = "/home/nebula/grpower/workspace/nebula/zircon"
    GARNET_PATH: str = "/home/nebula/grpower/workspace/nebula/garnet"
