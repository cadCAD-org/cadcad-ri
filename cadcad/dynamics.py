"""Blocks and Dynamics definitions."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence, Union

from cadcad.spaces import Space
from cadcad.trajectories import Point


def block(
    func: Union[
        Callable[
            [Union[Point, Sequence[Point]], Optional[Space]],
            Union[Point, Sequence[Point]],
        ],
        Callable[[Union[Point, Sequence[Point]]], Union[Point, Sequence[Point]]],
    ],
    param_space: Optional[Space] = None,
) -> Block:
    """_summary_

    Parameters
    ----------
    func : Callable
        _description_

    Returns
    -------
    Callable
        _description_
    """
    if isinstance(func.__annotations__["return"], Space):
        codomain = func.__annotations__["return"]
    else:
        codomain = None

    del func.__annotations__["return"]

    if isinstance(func.__annotations__["return"], Space):
        domain = func.__annotations__
    else:
        domain = None

    if not domain or not codomain:
        raise TypeError(
            "The block function must have spaces as the type of arguments and return"
        )

    return Block(func, domain, codomain, param_space)


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

    @property
    def domains(self) -> Union[Space, Sequence[Space]]:
        """Get the domains of the block."""
        return self.__domains

    @property
    def codomains(self) -> Union[Space, Sequence[Space]]:
        """Get the codomains of the block."""
        return self.__codomains

    @property
    def param_space(self) -> Optional[Space]:
        """Get the parameter space of the block."""
        return self.__param_space

    def name(self) -> str:
        """Get the name of the block."""
        return self.__function.__name__

    def __copy(self) -> Block:
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

    def __copy__(self) -> Block:
        """Forbidden copy method."""
        return self.__copy()

    def __deepcopy__(self, memo: dict) -> Block:
        """Forbidden copy method."""
        return self.__copy()

    def __str__(self) -> str:
        """Return a string representation of a space."""
        newline = "\n"

        str_result = f"Block {self.function.__name__} "
        str_result += f"has domains: {newline}-> {self.domains},{newline}"
        str_result += f"has codomains: {newline}-> {self.codomains},{newline}"

        if self.param_space:
            str_result += f"has parameter space {self.param_space} "

        return str_result

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("call")
