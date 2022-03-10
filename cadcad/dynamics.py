"""Blocks and Dynamics definitions."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, Callable, Union, Collection

from cadcad.trajectories import Point
from cadcad.spaces import Space
from cadcad.errors import FreezingError, CopyError


@dataclass
class Block():
    """Blocks in cadCAD.

    Attributes
    ----------
    dtype: type
        type of the dimension
    name : str
        name of the dimension (optional)
    description : str
        optional description of the dimension (optional)
    """

    __function: Callable[[Union[Point, Collection[Point]], Optional[Space]],
                         Union[Point, Collection[Point]]]
    __domains: Union[Space, Collection[Space]]
    __codomains: Union[Space, Collection[Space]]
    __param_space: Optional[Space] = None
    __name: Optional[str] = None
    __description: Optional[str] = None
    __frozen: bool = False

    @property
    def function(
        self
    ) -> Callable[[Union[Point, Collection[Point]], Optional[Space]], Union[
            Point, Collection[Point]]]:
        """Get the function of the block."""
        return self.__function

    @function.setter
    def function(
        self,
        function: Callable[[Union[Point, Collection[Point]], Optional[Space]],
                           Union[Point, Collection[Point]]]
    ) -> None:
        """Set the function of the block."""
        if not self.__frozen:
            self.__function = function
        else:
            raise FreezingError(Block)

    @property
    def domains(self) -> Union[Space, Collection[Space]]:
        """Get the domains of the block."""
        return self.__domains

    @domains.setter
    def domains(self, domains: Union[Space, Collection[Space]]) -> None:
        """Set Name."""
        if not self.__frozen:
            self.__domains = domains
        else:
            raise FreezingError(Block)

    @property
    def codomains(self) -> Union[Space, Collection[Space]]:
        """Get the codomains of the block."""
        return self.__codomains

    @codomains.setter
    def codomains(self, codomains: Union[Space, Collection[Space]]) -> None:
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

    def map(
        self, points: Union[Point, Collection[Point]]
    ) -> Union[Point, Collection[Point]]:
        """Execute the block's function onto points.

        Args:
            points (Union[Point, Collection[Point]]): input points for the block's function

        Returns:
            Union[Point, Collection[Point]]: output points
        """
        try:
            for point, space in zip(points, self.domains):
                if not point.space.is_equivalent(space):
                    raise ValueError(
                        "The point provided does not match the schema of the domain"
                    )
        except TypeError:
            if not points.space.is_equivalent(self.domains):
                raise ValueError(
                    "The point provided does not match the schema of the domain"
                ) from None

        result = self.function(points, self.param_space)

        try:
            for res, space in zip(result, self.codomains):
                if not res.space.is_equivalent(space):
                    raise ValueError(
                        "The point generated does not match the schema of the codomain"
                    )
        except TypeError:
            if not result.space.is_equivalent(self.codomains):
                raise ValueError(
                    "The point generated does not match the schema of the codomain"
                ) from None

        return result
