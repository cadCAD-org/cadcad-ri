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

    def __init__(self, space_name: str, expected: List[str], given: str) -> None:
        """Raise with default message."""
        self.message = (
            f"Wrong schema for space {space_name}. "
            + f"Expected one of {expected}, but was given [{given}]."
        )

        super().__init__(self.message)


class InstanceError(Exception):
    """Exception raised when trying to instantiate a cadCAD space type."""

    def __init__(self) -> None:
        """Raise with default message."""
        self.message = "Attempted to instance a space type."

        super().__init__(self.message)


class IllFormedError(Exception):
    """Exception raised when trying to decorate an ill formed class with @space."""

    def __init__(self) -> None:
        """Raise with default message."""
        self.message = "Attempted to decorate an ill formed class."

        super().__init__(self.message)


class WiringError(Exception):
    """Exception raised when the codomain of a given block does not *exactly match* the
    domain of the subsequent block."""

    def __init__(self, curr_block, next_block) -> None:
        curr_block_name = curr_block._Block__function.__name__
        next_block_name = next_block._Block__function.__name__
        curr_block_codomains = curr_block.codomain_names
        next_block_domains = curr_block.domain_names
        self.message = f"Block ({curr_block_name}) codomain ({curr_block_codomains}) does not *exactly match* subsequent block ({next_block_name}) domain ({next_block_domains})."

        super().__init__(self.message)


class BlockInputError(Exception):
    """Exception raised when the block input Point is not found in the block's domain."""

    def __init__(self, current_state, block) -> None:
        block_name = block._Block__function.__name__
        self.message = f"Block {block_name} requires Point[{block.domain_names}] as input; you passed Point[{current_state.space.name()}]"

        super().__init__(self.message)


class BlockOutputError(Exception):
    """Exception raised when the block output Point is not found in the block's codomain."""

    def __init__(self, block, next_state) -> None:
        block_name = block._Block__function.__name__
        self.message = f"Block {block_name} must return Point[{block.codomain_names}]; returned Point[{next_state.space.name()}] instead"

        super().__init__(self.message)
