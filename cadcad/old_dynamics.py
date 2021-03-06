"""Blocks and Dynamics definitions."""

from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Optional, Union

from cadcad.errors import CopyError, FreezingError
from cadcad.old_spaces import Space
from cadcad.trajectories import Point


@dataclass
class Block:
    """Blocks in cadCAD.

    Attributes
    ----------
    function: Callable
        function to be executed by the block
    domains: Space | Collection[Space]
        space(s) that incoming point(s) must adhere to
    codomains: Space | Collection[Space]
        space(s) that outgoing point(s) must adhere to
    param_space: Space
        parameter space of the block (optional)
    name : str
        name of the dimension (optional)
    description : str
        optional description of the dimension (optional)
    frozen: bool
        whether the dimension is immutable or not. Defaults to False
    """

    __function: Union[
        Callable[
            [Union[Point, Sequence[Point]], Optional[Space]],
            Union[Point, Sequence[Point]],
        ],
        Callable[[Union[Point, Sequence[Point]]], Union[Point, Sequence[Point]]],
    ]
    __domains: Union[Space, Sequence[Space]]
    __codomains: Union[Space, Sequence[Space]]
    __param_space: Optional[Space] = None
    __name: Optional[str] = None
    __description: Optional[str] = None
    __frozen: bool = False

    @property
    def function(
        self,
    ) -> Union[
        Callable[
            [Union[Point, Sequence[Point]], Optional[Space]],
            Union[Point, Sequence[Point]],
        ],
        Callable[[Union[Point, Sequence[Point]]], Union[Point, Sequence[Point]]],
    ]:
        """Get the function of the block."""
        return self.__function

    @function.setter
    def function(
        self,
        function: Callable[
            [Union[Point, Sequence[Point]], Optional[Space]],
            Union[Point, Sequence[Point]],
        ],
    ) -> None:
        """Set the function of the block."""
        if not self.__frozen:
            self.__function = function
        else:
            raise FreezingError(Block)

    @property
    def domains(self) -> Union[Space, Sequence[Space]]:
        """Get the domains of the block."""
        return self.__domains

    @domains.setter
    def domains(self, domains: Union[Space, Sequence[Space]]) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__domains = domains
        else:
            raise FreezingError(Block)

    @property
    def codomains(self) -> Union[Space, Sequence[Space]]:
        """Get the codomains of the block."""
        return self.__codomains

    @codomains.setter
    def codomains(self, codomains: Union[Space, Sequence[Space]]) -> None:
        """Set the codomains of the block."""
        if not self.__frozen:
            self.__codomains = codomains
        else:
            raise FreezingError(Block)

    @property
    def param_space(self) -> Optional[Space]:
        """Get the parameter space of the block."""
        return self.__param_space

    @param_space.setter
    def param_space(self, param_space: Optional[Space]) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__param_space = param_space
        else:
            raise FreezingError(Block)

    @property
    def name(self) -> Optional[str]:
        """Get the name of the block."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__name = name
        else:
            raise FreezingError(Block)

    @property
    def description(self) -> Optional[str]:
        """Get the description of the block."""
        return self.__description

    @description.setter
    def description(self, description: Optional[str]) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__description = description
        else:
            raise FreezingError(Block)

    def freeze(self) -> None:
        """Freeze the block to deny further changes to it.

        NOTE: This action is irreversible.
        """
        self.__frozen = True

    def is_frozen(self) -> bool:
        """Get freezing status."""
        return self.__frozen

    def copy(self) -> Block:
        """Make a deep copy of a block object.

        The resulting block will be mutable. Inherits all other atributes from the parent block.

        Returns:
            Block: new block
        """
        cls = self.__class__
        new_blk = cls.__new__(cls)
        internal_dict = deepcopy(self.__dict__)
        internal_dict["_Block__frozen"] = False
        new_blk.__dict__.update(internal_dict)
        return new_blk

    def __copy__(self) -> None:
        """Forbidden copy method."""
        raise CopyError(Space)

    def __deepcopy__(self, memo: dict) -> None:
        """Forbidden copy method."""
        raise CopyError(Space)

    def __str__(self) -> str:
        """Return a string representation of a space."""
        newline = "\n"
        str_result = ""

        if self.is_frozen():
            str_result += "Frozen block "
        else:
            str_result += "Unfrozen block "

        if self.name:
            str_result += f"{self.name} "

        str_result += f"with function {self.function.__name__} "
        str_result += f"has domains: {newline}-> {self.domains},{newline}"
        str_result += f"has codomains: {newline}-> {self.codomains},{newline}"

        if self.param_space:
            str_result += f"has parameter space {self.param_space} "

        if self.description:
            str_result += f"and description {self.description}"

        return str_result

    def map(
        self, points: Union[Point, Sequence[Point]]
    ) -> Union[Point, Sequence[Point]]:
        """Execute the block's function onto points.

        Args:
            points (Union[Point, Collection[Point]]): input points for the block's function
        Raises:
            ValueError: if any point doesn't conform to the space(s)
        Returns:
            Union[Point, Collection[Point]]: output points
        """
        if isinstance(points, Point) and isinstance(self.domains, Space):
            if not points.space.is_equivalent(self.domains):
                raise ValueError(
                    "The point provided does not match the schema of the domain"
                )
        elif (
            isinstance(points, Point)
            and isinstance(self.domains, Sequence)
            and len(self.domains) == 1
        ):
            if not points.space.is_equivalent(self.domains[0]):
                raise ValueError(
                    "The point provided does not match the schema of the domain"
                )
        elif isinstance(points, Sequence) and isinstance(self.domains, Sequence):
            for point, space in zip(points, self.domains):
                if not point.space.is_equivalent(space):
                    raise ValueError(
                        "The point provided does not match the schema of the domain"
                    )
        else:
            raise TypeError("Inapropriate argument for points on the map method")

        if self.param_space:
            result = self.function(points, self.param_space)
        else:
            result = self.function(points)

        if isinstance(result, Point) and isinstance(self.codomains, Space):
            if not result.space.is_equivalent(self.codomains):
                raise ValueError(
                    "The point generated does not match the schema of the codomain"
                )
        elif (
            isinstance(result, Point)
            and isinstance(self.domains, Sequence)
            and len(self.domains) == 1
        ):
            if not result.space.is_equivalent(self.domains[0]):
                raise ValueError(
                    "The point provided does not match the schema of the domain"
                )
        elif isinstance(result, Sequence) and isinstance(self.codomains, Sequence):
            for res, space in zip(result, self.codomains):
                if not res.space.is_equivalent(space):
                    raise ValueError(
                        "The point generated does not match the schema of the codomain"
                    )
        else:
            raise TypeError("The object generated is not a Point")

        return result
