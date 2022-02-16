"""Dimensions definition."""

from dataclasses import dataclass
from cadcad.utils import FreezingError


@dataclass(eq=False)
class Dimension():
    """Dimensions in cadCAD.

    Attributes
    ----------
    dtype: type
        type of the dimension
    name : str
        name of the dimension
    description : str
        optional description of the dimension
    frozen : bool
        wether the dimension is immutable or not
    """

    __dtype: type
    __name: str
    __description: str = ""
    _frozen: bool = False

    @property
    def name(self) -> str:
        """Get Name."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set Name."""
        if not self._frozen:
            self.__name = name
        else:
            raise FreezingError

    @property
    def dtype(self) -> type:
        """Get Dtype."""
        return self.__dtype

    @dtype.setter
    def dtype(self, dtype: type) -> None:
        """Set Dtype."""
        if not self._frozen:
            self.__dtype = dtype
        else:
            raise FreezingError

    @property
    def description(self) -> str:
        """Get Description."""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        """Set Description."""
        if not self._frozen:
            self.__description = description
        else:
            raise FreezingError

    def is_frozen(self) -> bool:
        """Get freezing status."""
        return self._frozen

    def freeze(self) -> None:
        """Freeze the dimension to deny further changes to it.

        NOTE: This action is irreversible.
        """
        self._frozen = True

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

        raise NotImplementedError

    def __str__(self) -> str:
        """Return a string representation of a dimension."""
        newline = '\n'

        if not self._frozen and self.__description:
            return (
                f'Mutable dimension {self.name} has data type {self.dtype} '
                f'and the following description: {newline}{self.description}{newline}'
            )
        elif not self._frozen and not self.__description:
            return f'Mutable dimension {self.name} has data type {self.dtype} and no description'
        elif self._frozen and not self.__description:
            return f'Frozen dimension {self.name} has data type {self.dtype} and no description'
        else:
            return (
                f'Frozen dimension {self.name} has data type {self.dtype} '
                f'and the following description: {newline}{self.description}{newline}'
            )
