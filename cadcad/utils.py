"""Utilities to be used by any cadCAD module."""


class FreezingError(Exception):
    """Exception raised when trying to change a frozen cadCAD object."""

    def __init__(self) -> None:
        """Raise with default message."""
        self.message = "Attempted to change a frozen Dimension."
        super().__init__(self.message)
