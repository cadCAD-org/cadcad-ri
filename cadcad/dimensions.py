"""Dimensions definition."""

from dataclasses import dataclass


@dataclass(eq=False)
class Dimension():
    """Dimensions in cadCAD."""

    __name: str
    __dtype: type  # should this be a union?
    __description: str = ""
    __frozen: bool = False

    @property
    def name(self) -> str:
        """Get Name."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__name = name
        else:
            raise Exception("Attempted to change a frozen Dimension.")

    @property
    def dtype(self) -> type:
        """Get Dtype."""
        return self.__dtype

    @dtype.setter
    def dtype(self, dtype: type) -> None:
        """Set Dtype."""
        if not self.__frozen:
            self.__dtype = dtype
        else:
            raise Exception("Attempted to change a frozen Dimension.")

    @property
    def description(self) -> str:
        """Get Description."""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        """Set Description."""
        if not self.__frozen:
            self.__description = description
        else:
            raise Exception("Attempted to change a frozen Dimension.")

    def is_frozen(self) -> bool:
        """Get freezing status."""
        return self.__frozen

    def freeze(self) -> None:
        """Freeze the dimension to deny further changes to it.

        NOTE: This action is irreversible.
        """
        self.__frozen = True

    def __eq__(self, other: object) -> bool:
        """Check if a dimension is equal to another.

        A dimension is equal to another if their dtype and name are equal.
        Even if the objects are equal, they may ocuppy different positions in memory.
        Args:
            other (Dimension): another dimension to compare
        Returns:
            bool: whether the dimension are equal or not
        """
        if isinstance(other, Dimension):
            return self.dtype == other.dtype and self.name == other.name

        return NotImplemented

    def __str__(self) -> str:
        """Return a string representation of a dimension."""
        return f'Dimension {self.name} has data type {self.dtype}'
