"""Error utilities to be used by any cadCAD module."""

from typing import List


class FreezingError(Exception):
    """Exception raised when trying to change a frozen cadCAD object."""

    def __init__(self, obj_type: type) -> None:
        """Raise with default message."""
        self.message = f"Attempted to change a frozen {obj_type} object."
        super().__init__(self.message)


class CopyError(Exception):
    """Exception raised when trying to copy a cadCAD object through the `copy` library."""

    def __init__(self, obj_type: type) -> None:
        """Raise with default message."""
        self.message = f"Attempted to copy a {obj_type} object through the copy library."
        super().__init__(self.message)


class SchemaError(Exception):
    """Exception raised when trying to instantiate a cadCAD point not obeying the space schema."""

    def __init__(self, space_name: str, expected: List[str],
                 given: str) -> None:
        """Raise with default message."""
        self.message = f"Wrong schema for space {space_name}. " +\
            f"Expected one of {expected}, but was given [{given}]."

        super().__init__(self.message)
