# -*- coding: utf-8 -*-

"""
Custom exception classes for the Release Note Generator script.
"""

class GitOperationException(Exception):
    """Exception raised for errors in Git operations."""
    pass

class ManifestParseException(Exception):
    """Exception raised for errors in manifest parsing."""
    pass

class PatchManagementException(Exception):
    """Exception raised for errors in patch management."""
    pass

class ReleaseNoteException(Exception):
    """Exception raised for errors in release note generation."""
    pass
