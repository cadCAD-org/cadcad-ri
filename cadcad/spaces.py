"""Dimensions and Spaces definitions.

To be redefined as a class factory
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Union

from frozendict import frozendict

from cadcad.errors import CopyError, FreezingError


class Space():
    """Spaces are the most fundamental building blocks of cadCAD."""

    def __init__(self,
                 name: str,
                 schema: Dict[str, Union[Dict[str, Any], type]],
                 description: Optional[str] = None,
                 constraints: Dict[str, Block] = {},
                 frozen: bool = False):
        """Construct a cadCAD space.

        Args:
            name (str): the name of the space
            schema (Dict[str, Union[Dict[str, Any], type]]): the type schema of the space
            description (Optional[str]): the description of the space. Defaults to None.
            frozen (bool, optional): wether the space is frozen or not. Defaults to False.

        Raises:
            ValueError: if the schema of the space contains a value that is not a type
        """
        self.__frozen: bool = frozen
        self.__name = name
        self.__description = description

        for value in Space.flatten_schema_types(schema):
            if not isinstance(type, type(value)):
                raise ValueError(
                    "The schema can only contain string to type pairs.")

        self.__schema: Dict[str, Union[Dict[str, Any], type]] = schema

    @property
    def schema(self) -> frozendict:
        """Get the schema of the space as a immutable view."""
        return frozendict(self.__schema)

    @property
    def name(self) -> str:
        """Get the name of the space."""
        return self.__name

    @property
    def constraint(self) -> str:
        """Get the name of the space."""
        return self.constraint

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

    my_space = Space('a', {
        'a': int
    }).add_constraint('is_positive', is_positive)

    def is_positive():
        pass

    def add_constraint(self, constraint_name: str,
                       constraint_func: Block) -> None:
        if self.is_frozen():
            raise FreezingError(Space)
        elif isinstance(constraint_name, str) and isinstance(
                constraint_func, Callable):
            # TODO: Crete a block here
            self.constraint[constraint_name] = constraint_func
        else:
            raise

    def create_constraint(self, constraint_name: str,
                          constraint_func: Callable) -> None:
        if self.is_frozen():
            raise FreezingError(Space)
        elif isinstance(constraint_name, str) and isinstance(
                constraint_func, Callable):
            # TODO: Crete a block here
            self.constraint[constraint_name] = constraint_func
        else:
            raise

    def add_dimensions(
            self, dimensions: Dict[str, Union[Dict[str, Any], type]]) -> None:
        """Add a dimension to an existing space's schema.

        Args:
            dimensions (Dict[str, Union[Dict[str, Any], type]]): dimensions to add as a dictionary
        Raises:
            ValueError: if there is a collision of dimension names and a new name is not given
        """
        if self.is_frozen():
            raise FreezingError(Space)

        for key, value in dimensions.items():
            if key in self.__schema.keys():
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

        try:
            del self.__schema[dim_name]
        except KeyError:
            print(f'The dimension "{dim_name}" is not present in {self.name}')
            raise

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

        for dim_name in self.__schema.keys():
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
        return not bool(self.__schema)

    def is_equivalent(self, other: Any) -> bool:
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

    def pretty_schema(self) -> str:
        """Return pretty string repreentation of the schema."""
        return json.dumps(self.__schema, indent=4, default=str)

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
        newline = '\n'
        str_result = ''
        dims = Space.flatten_schema_keys(self.__schema)

        if self.is_frozen():
            str_result += "Frozen space "
        else:
            str_result += "Unfrozen space "

        str_result += f"{self.name} "
        str_result += f"has dimensions {dims} "

        if self.description:
            str_result += f"and description:{newline}{self.description}{newline}"

        return str_result

    def __mul__(self: Space, other: Any) -> Space:
        """Do a cartesian product of self and other."""
        if isinstance(other, Space):
            new_name = f"{self.name} x {other.name}"

            new_space = Space({}, new_name)

            new_space.add_dimensions(self.__schema)
            new_space.add_dimensions(other.schema)

            return new_space

        raise ValueError(f"Impossible to multiply a space to a {type(other)}")

    def __getitem__(self, key: str) -> Union[Dict[str, Any], type]:
        """Get dimension on space through indexing."""
        return self.__schema[key]

    @staticmethod
    def flatten_schema_types(
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
                yield from Space.flatten_schema_types(value)
            else:
                yield value

    @staticmethod
    def flatten_schema_keys(
            dimensions: Dict[str, Union[Dict[str, Any], type]]) -> List[str]:
        """Yield the values of the nested dictionary that is the dimensions of a space.

        Args:
            dimensions (Dict[str, Union[Dict[str, Any], type]]): the dimensions of the space

        Yields:
            List[str]: list of dimension names from the dimensions dictionary
        """
        schema_keys = []

        for key, value in dimensions.items():
            if isinstance(value, dict):
                schema_keys.append(key)
                schema_keys += Space.flatten_schema_keys(value)
            else:
                schema_keys.append(key)

        return schema_keys
