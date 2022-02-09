"""
Space definition.

[TODO: Document the usage]
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import List, Optional, Set, Dict


@dataclass(frozen=True, eq=False)
class Space():
    """
    Spaces in cadCAD.

    [TODO: Document the usage]
    """

    __name: str
    __dimensions: Set[Dimension] = set()

    @property
    def name(self) -> str:
        """Name getter."""
        return self.__name

    @property
    def dimensions(self) -> Set[Dimension]:
        """Dimensions getter."""
        return self.__dimensions

    def copy(self) -> Space:
        """Make a copy of the space object."""
        return replace(self)

    def derive(self, dims: List[Dimension]) -> Space:
        """Derive a new space from self by adding more dimensions.

        Args:
            dims (List[Dimension]): set of dimensions to add

        Returns:
            Space: new derived space
        """
        dim_set = self.dimensions.union(set(dims))

        return Space(f'derived-{self.__name}', dim_set)

    def subspace(self, subdims: List[str]) -> Space:
        """Make a subspace with dimensions subdims if subdims is a subset of the dimensions of self.

        Args:
            subdims (List[str]): list of names of dimensions to be present at the subspace

        Raises:
            Exception: if there is no common dimensions between subdims and self

        Returns:
            Space: new space that has a subset of dimensions from self
        """
        dim_list = set()

        for dim_name in subdims:
            result = self.__search_dim(dim_name)
            if result is not None:
                dim_list.add(result)

        if not dim_list:
            raise Exception(
                f'Space {self.__name} does not contain the dimensions you ask for'
            )

        return Space(f'sub-{self.__name}', dim_list)

    def is_equivalent(self, other: Space) -> bool:
        """Check if a space is equivalent to another space.

        Equivalence is having the same dimensions but not necessarily the same name.

        Args:
            other (Space): space to compare to

        Returns:
            bool: whether the spaces are equivalent or not
        """
        return self.dimensions == other.dimensions

    def __search_dim(self, dim_name: str) -> Optional[Dimension]:
        """Search for a certain dimension on self by it's name.

        Args:
            dim_name (str): name of the dimension to search

        Returns:
            Optional[Dimension]: either the dimension that was found or None
        """
        for dim in self.dimensions:
            if dim.name == dim_name:
                return dim
        return None

    def __eq__(self, other: object) -> bool:
        """Check if a space is equal to another.

        A space is equal to another if their dimensions and name are equal.
        Even if the objects are equal, they may ocuppy different positions in memory.

        Args:
            other (Space): another space to compare

        Returns:
            bool: whether the spaces are equal or not
        """
        if isinstance(other, Space):
            return self.dimensions == other.dimensions and self.name == other.name

        return NotImplemented

    def __str__(self) -> str:
        """Return a string representation of a space."""
        newline = '\n'
        attributes = ''.join(f"{dim.name}: {dim.dtype}{newline}"
                             for dim in self.dimensions)

        return f'Space {self.name} has dimensions:{newline}{attributes}{newline}'

    # def __mul__(self: Space, other: Space) -> Space:
    #     """[summary].

    #     Args:
    #         other (MetaSpace): [description]

    #     Returns:
    #         MetaSpace: [description]
    #     """

    # def __imul__(self: Space, other: Space) -> Space:
    #     """[summary].

    #     Args:
    #         self (MetaSpace): [description]
    #         other (MetaSpace): [description]

    #     Returns:
    #         MetaSpace: [description]
    #     """


# S3 = S1 * S2
# S1 *= S2

# S1 -> prey: int pred: int
# S2 -> prey: int flora: int
# S3 -> prey: int pred: int flora: int


@dataclass(frozen=True, eq=False)
class Dimension():
    """
    Dimensions in cadCAD.

    [TODO: Document the usage]
    """

    __name: str
    __dtype: type

    @property
    def name(self) -> str:
        """Name getter."""
        return self.__name

    @property
    def dtype(self) -> type:
        """Dtype getter."""
        return self.__dtype

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


def from_dict(name: str, dims: Dict[str, type]) -> Space:
    """Create a space from a name and dictionary of strings and types pairs.

    Each entry of the dictionary will be transformed into a Dimension object.

    Args:
        name (str): name of the space
        dims (Dict[str, type]): dictionary of strings and types pairs

    Returns:
        Space: [description]
    """
    dims_set = {Dimension(name, dtype) for name, dtype in dims.items()}

    return Space(name, dims_set)
