"""Dimensions and Spaces definitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Iterator, Optional, Sequence, Dict, Union, Any

from frozendict import frozendict

from cadcad.errors import FreezingError, CopyError


class Space():
    """Spaces are the most fundamental building blocks of cadCAD."""

    def __init__(self,
                 schema: Dict[str, Union[Dict[str, Any], type]],
                 name: str,
                 description: Optional[str] = None,
                 frozen: bool = False):
        """Construct a cadCAD space.

        Args:
            schema (Dict[str, Union[Dict[str, Any], type]]): the type schema of the space
            name (str): the name of the space
            description (Optional[str]): the description of the space. Defaults to None.
            frozen (bool, optional): wether the space is frozen or not. Defaults to False.

        Raises:
            ValueError: if the schema of the space contains a value that is not a type
        """
        self.__frozen: bool = frozen
        self.__name = name
        self.__description = description

        for value in Space.flatten_dims(schema):
            if not isinstance(type, type(value)):
                raise ValueError(
                    "The schema can only contain string to type pairs.")

        self.__schema: Dict[str, Union[Dict[str, Any], type]] = schema

    @property
    def schema(self) -> frozendict:
        """Get the schema of the space."""
        return frozendict(self.__schema)

    @property
    def name(self) -> str:
        """Get the name of the space."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the space."""
        if not self.__frozen:
            self.__name = name
        else:
            raise FreezingError(Space)

    @property
    def description(self) -> Optional[str]:
        """Get the description of the space."""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        """Set the description of the space."""
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

    def add_dimensions(
            self, dimensions: Dict[str, Union[Dict[str, Any], type]]) -> None:
        """Add a dimension to an existing space's schema.

        Args:
            dim (Dict[str, type]): dimension to add
            new_name (Optional[str]): name to be given to a dimension if there is a name collision
        Raises:
            ValueError: if there is a collision of dimension names and a new name is not given
        """
        if self.is_frozen():
            raise FreezingError(Space)

        for key, value in dimensions.items():
            if key in self.schema.keys():
                raise ValueError(f"Collision of dimension names. \
                Rename the key {key} of your dimensions dictionary.")

            self.__schema[key] = value

    def drop_dimension(self, dim_name: str) -> None:
        """Remove a dimension from a space's schema by it's name.

        Args:
            dim_name (str): name of dimension to be removed
        """
        if self.is_frozen():
            raise FreezingError(Space)

        del self.__schema[dim_name]

    def subspace(self, subdims: Sequence[str]) -> Space:
        """Make a mutable subspace with dimensions subdims.

        If there is no dimension in subdims that are present in self, it returns an empty Space.

        Args:
            subdims (Sequence[str]): list of names of dimensions to be present at the subspace
        Returns:
            Space: new space that has a subset of dimensions from self
        """
        cls = self.__class__
        new_space = cls.__new__(cls)
        internal_dict = deepcopy(self.__dict__)
        internal_dict["_Space__frozen"] = False

        for dim_name in self.schema.keys():
            if dim_name not in subdims:
                del internal_dict["_Space__schema"][dim_name]

        new_space.__dict__.update(internal_dict)

        return new_space

    def is_empty(self) -> bool:
        """Check if a space is empty.

        A space is empty if it has no dimensions (it's schema is empty).

        Returns:
            bool: whether the space is empty or not
        """
        return not bool(self.schema)

    def is_equivalent(self, other: Space) -> bool:
        """Check if a space is equivalent to another space.

        Equivalence is having the same dimensions but not necessarily the other atributes.
        Args:
            other (Space): space to compare to
        Returns:
            bool: whether the spaces are equivalent or not
        """
        if isinstance(other, Space):
            return self.schema == other.schema

        raise ValueError(f"Impossible to compare a space with a {type(other)}")

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
            return self.schema == other.schema and self.name == other.name \
                and self.description == other.description

        raise ValueError(f"Impossible to compare a space with a {type(other)}")

    def __str__(self) -> str:
        """Return a string representation of a space."""
        str_result = ""
        dims = tuple(self.schema.keys())

        if self.is_frozen():
            str_result += "Frozen space "
        else:
            str_result += "Unfrozen space "

        str_result += f"{self.name} "
        str_result += f"has dimensions {dims}"

        if self.description:
            str_result += f"and description {self.description}"

        return str_result

    def __mul__(self: Space, other: Space) -> Space:
        """Do a cartesian product of self and other."""
        if isinstance(other, Space):
            new_name = f"{self.name} x {other.name}"

            new_space = Space({}, new_name)

            new_space.add_dimensions(self.schema)
            new_space.add_dimensions(other.schema)

            return new_space

        raise ValueError(f"Impossible to multiply a space to a {type(other)}")

    def __getitem__(self, key: str) -> Union[Dict[str, Any], type]:
        """Get dimension on space through indexing."""
        return self.schema[key]

    @staticmethod
    def flatten_dims(
            dimensions: Dict[str, Union[Dict[str, Any],
                                        type]]) -> Iterator[type]:
        """Yield the values of the nested dictionary that is the dimensions of a space.

        Args:
            dimensions (Dict[str, Union[Dict[str, Any], type]]): the dimensions of the space

        Yields:
            Iterator[type]: the value inside the dictionary
        """
        for value in dimensions.values():
            if isinstance(value, dict):
                yield from Space.flatten_dims(value)
            else:
                yield value
