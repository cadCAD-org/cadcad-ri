"""Dimensions and Spaces definitions."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Collection, Dict

from cadcad.errors import FreezingError, CopyError


class Space():
    """
    Spaces in cadCAD.

    Attributes
    ----------
    dim_tuple (Tuple[Dimension]):
        dictionary of dimension names to dimensions that make up the set of dimensions of the space
    name: str
        name of the space
    description: str
        description of the space. (optional)
    dim_names Tuple[str]:
        _description_ (optional). Defaults to None.
    frozen : bool
        whether the dimension is immutable or not

    Raises:
            ValueError: if there is a collision of dimension names
            ValueError: if there is a length mismatch between dim_tuple and dim_names
    """

    def __init__(self,
                 dim_tuple: Collection[Dimension],
                 name: str,
                 description: str = "",
                 dim_names: Optional[Collection[str]] = None,
                 frozen: bool = False):
        """Build a space based on a tuple of dimensions."""
        self.__frozen: bool = frozen
        self.__name = name
        self.__description = description

        if dim_names and len(dim_names) != len(dim_tuple):
            raise ValueError(
                "Length mismatch between dim_tuple and dim_names.")

        self.__dimensions: Dict[str, Dimension] = {}

        if dim_names:
            for (internal_name, dim) in zip(dim_names, dim_tuple):
                self.__dimensions[internal_name] = dim
        else:
            for dim in dim_tuple:
                if dim.name in self.__dimensions:
                    raise ValueError("""Collision of dimension names. \
                            Use dim_names to rename your dimensions inside the space."""
                                     )

                self.__dimensions[dim.name] = dim

    @property
    def dimensions(self) -> Dict[str, Dimension]:
        """Get Dimensions."""
        return self.__dimensions

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
            raise FreezingError(Space)

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
            raise FreezingError(Space)

    def is_frozen(self) -> bool:
        """Get freezing status."""
        return self.__frozen

    def freeze(self) -> None:
        """Freeze the space to deny further changes to it.

        NOTE: This action is irreversible.
        """
        self.__frozen = True

    def add_dimension(self,
                      dim: Dimension,
                      new_name: Optional[str] = None) -> None:
        """Add a dimension to an existing space.

        Args:
            dim (Dimension): dimension to add
            new_name (Optional[str]): name to be given to a dimension if there is a name collision
        Raises:
            ValueError: if there is a collision of dimension names
        """
        if self.is_frozen():
            raise FreezingError(Space)

        if dim.name in self.dimensions and not new_name:
            raise ValueError("Collision of dimension names. \
                Rename your dimensions or use new_name to rename inside the space."
                             )

        if new_name:
            self.dimensions[new_name] = dim
        else:
            self.dimensions[dim.name] = dim

    def drop_dimension(self, dim_name: str) -> None:
        """Remove a dimension from a space by it's name.

        Args:
            dim_name (str): name of dimension to be removed
        """
        del self.dimensions[dim_name]

    def augment(self,
                dims: Collection[Dimension],
                auto_naming: bool = False) -> Space:
        """Derive a new mutable space from self by adding more dimensions.

        Args:
            dims (Tuple[Dimension]): tuple of dimensions to add
        Returns:
            Space: new derived space
        """
        new_space = self.copy()

        for dim in dims:
            if dim in new_space.dimensions.values() and auto_naming:
                new_space.add_dimension(dim, f"new_{dim.name}")
            else:
                new_space.add_dimension(dim)

        return new_space

    def subspace(self, subdims: Collection[str]) -> Space:
        """Make a mutable subspace with dimensions subdims.

        If there is no dimension in subdims that are present in self, it returns an empty Space.

        Args:
            subdims (Tuple[str]): list of internal names of dimensions to be present at the subspace
        Returns:
            Space: new space that has a subset of dimensions from self
        """
        cls = self.__class__
        new_space = cls.__new__(cls)
        internal_dict = deepcopy(self.__dict__)
        internal_dict["_Space__frozen"] = False

        for dim in self.dimensions.values():
            if dim.name not in subdims:
                del internal_dict["_Space__dimensions"][dim.name]

        new_space.__dict__.update(internal_dict)

        return new_space

    def is_empty(self) -> bool:
        """Check if a space is empty.

        A space is empty if it has no dimensions.

        Returns:
            bool: whether the space is empty or not
        """
        return not bool(self.dimensions)

    def is_equivalent(self, other: Space) -> bool:
        """Check if a space is equivalent to another space.

        Equivalence is having the same dimensions but not necessarily the other atributes.
        Args:
            other (Space): space to compare to
        Returns:
            bool: whether the spaces are equivalent or not
        """
        return self.dimensions == other.dimensions

    @staticmethod
    def from_dict(dims: Dict[str, Dimension], name: str) -> Space:
        """Create a mutable space from a name and dictionary of string and dimension pairs.

        Each entry of the dictionary will be transformed into a Dimension object.

        Args:
            name (str): name of the space
            dims (Dict[str, type]): dictionary of strings and types pairs
        Returns:
            Space: [description]
        """
        dim_tuple = tuple(dims.values())
        dim_names = tuple(dims.keys())
        return Space(name=name, dim_tuple=dim_tuple, dim_names=dim_names)

    def copy(self) -> Space:
        """Make a deep copy of a space object.

        The resulting space will be mutable. Inherits all other atributes from the parent space.

        Returns:
            Space: new space
        """
        cls = self.__class__
        new_space = cls.__new__(cls)
        internal_dict = deepcopy(self.__dict__)
        internal_dict["_Space__frozen"] = False
        new_space.__dict__.update(internal_dict)
        return new_space

    def __copy__(self) -> None:
        """Forbidden copy method."""
        raise CopyError(Space)

    def __deepcopy__(self, memo: dict) -> None:
        """Forbidden copy method."""
        raise CopyError(Space)

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
            return self.dimensions == other.dimensions and self.name == other.name \
                and self.description == other.description

        raise NotImplementedError

    def __str__(self) -> str:
        """Return a string representation of a space."""
        newline = '\n'
        dims = tuple(self.dimensions.keys())

        if not self.__frozen and self.description:
            return (
                f'Mutable space {self.name} has dimensions {dims} '
                f'and the following description:{newline}{self.description}{newline}'
            )
        if not self.__frozen and not self.description:
            return f'Mutable space {self.name} has dimensions {dims} and no description'
        if self.__frozen and not self.description:
            return f'Frozen space {self.name} has dimensions {dims} and no description'
        return (
            f'Frozen space {self.name} has dimensions {dims} '
            f'and the following description:{newline}{self.description}{newline}'
        )

    def __mul__(self: Space, other: Space) -> Space:
        """Do a cartesian product of self and other."""
        if isinstance(other, Space):
            new_name = f"{self.name} x {other.name}"

            dim_tuple = tuple(other.dimensions.values())

            new_space = self.augment(dim_tuple, True)
            new_space.name = new_name

            return new_space

        raise NotImplementedError

    def __getitem__(self, key: str) -> Dimension:
        """Get dimension on space through indexing."""
        return self.dimensions[key]


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
        optional description of the dimension (optional)
    frozen : bool
        whether the dimension is immutable or not
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
            raise FreezingError(Dimension)

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
            raise FreezingError(Dimension)

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
            raise FreezingError(Dimension)

    def is_frozen(self) -> bool:
        """Get freezing status."""
        return self._frozen

    def freeze(self) -> None:
        """Freeze the dimension to deny further changes to it.

        NOTE: This action is irreversible.
        """
        self._frozen = True

    def copy(self, name: str = "", description: str = "") -> Dimension:
        """Make a deep copy of a dimension object.

        The resulting object will be mutable. Inherits all other atributes from the parent object.

        Args:
            name (str, optional): Optional name of the new dimension. Defaults to "".
            description (str, optional): Optional description of the new dimension. Defaults to "".

        Returns:
            Dimension: new dimension
        """
        cls = self.__class__
        result = cls.__new__(cls)
        internal_dict = deepcopy(self.__dict__)
        internal_dict["_frozen"] = False
        result.__dict__.update(internal_dict)
        if name:
            result.name = name
        if description:
            result.description = description
        return result

    def __copy__(self) -> Dimension:
        """Overriden copy method to custom copy."""
        return self.copy()

    def __deepcopy__(self, memo: dict) -> Dimension:
        """Overriden copy method to custom copy."""
        return self.copy()

    def __eq__(self, other: object) -> bool:
        """Check if a dimension is equal to another.

        A dimension is equal to another if their dtype, name and description are equal.
        Even if the objects are equal, they may ocuppy different positions in memory.

        Args:
            other (Dimension): another dimension to compare
        Returns:
            bool: whether the dimension are equal or not
        """
        if isinstance(other, Dimension):
            return self.dtype == other.dtype and self.name == other.name \
                and self.description == other.description

        raise NotImplementedError

    def __str__(self) -> str:
        """Return a string representation of a dimension."""
        newline = '\n'

        if not self._frozen and self.__description:
            return (
                f'Mutable dimension {self.name} has data type {self.dtype} '
                f'and the following description:{newline}{self.description}{newline}'
            )
        if not self._frozen and not self.__description:
            return f'Mutable dimension {self.name} has data type {self.dtype} and no description'
        if self._frozen and not self.__description:
            return f'Frozen dimension {self.name} has data type {self.dtype} and no description'
        return (
            f'Frozen dimension {self.name} has data type {self.dtype} '
            f'and the following description:{newline}{self.description}{newline}'
        )

    def is_equivalent(self, other: Dimension) -> bool:
        """Check if a dimension is equivalent to another.

        Args:
            other (Dimension): another dimension to compare

        Returns:
            bool: whether the dimension are equivalent or not
        """
        if isinstance(other, Dimension):
            return self.dtype == other.dtype

        raise NotImplementedError
