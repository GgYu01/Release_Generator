# utils/exception_handler.py

class AppException(Exception):
    """
    Base exception class for application-specific exceptions.

    Attributes:
        message (str): Human-readable message describing the exception.
        error_code (int): Numeric error code associated with the exception.
    """
    def __init__(self, message: str, error_code: int = 0):
        self.message = message
        self.error_code = error_code
        super().__init__(f"[Error {error_code}] {message}")


class GitException(AppException):
    """Exception raised for Git operation errors."""
    pass


class ManifestException(AppException):
    """Exception raised for Manifest parsing errors."""
    pass


class ConfigurationException(AppException):
    """Exception raised for Configuration errors."""
    pass


# More specific exceptions can be defined as needed