"""Exceptions for API-related errors."""


class MaxRetriesExceeded(Exception):
    """Raised when the maximum number of retries for an API request is exceeded."""
