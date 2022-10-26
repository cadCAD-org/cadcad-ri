"""Blocks and Dynamics definitions."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Collection, List, Optional, Union, get_args

from cadcad.points import Point, TSpace_co
from cadcad.spaces import Space


def block(
    func: Callable[
        [Union[Point[TSpace_co], Collection[Point[TSpace_co]]]],
        Union[Point[TSpace_co], Collection[Point[TSpace_co]]],
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
    func_annotations = deepcopy(func.__annotations__)

    if not func_annotations:
        raise ValueError("The block function must be type annotated")

    return_type = func_annotations["return"]
    specialized_type = get_args(return_type)[0]

    if issubclass(return_type.__origin__, Point) and isinstance(
        specialized_type, Space
    ):
        codomain: Union[Point[Space], Collection[Point[Space]]] = return_type
    elif (
        isinstance(return_type, Collection)
        and isinstance(specialized_type, Point)
        and isinstance(get_args(specialized_type)[0], Space)
    ):
        codomain = return_type
    else:
        raise TypeError(
            "The return of a block function must be a point of a space or a collection of them."
        )

    del func_annotations["return"]

    if len(func_annotations) != 1:
        raise ValueError("The block function must have exactly one argument")

    domain_type = tuple(func_annotations.values())[0]
    specialized_domain_type = get_args(domain_type)[0]

    if issubclass(domain_type.__origin__, Point) and isinstance(
        specialized_domain_type, Space
    ):
        domain = domain_type
    elif (
        isinstance(domain_type, Collection)
        and isinstance(specialized_domain_type, Point)
        and isinstance(get_args(specialized_domain_type)[0], Space)
    ):
        domain = domain_type  # type: ignore
    else:
        raise TypeError(
            "The domain of a block function must be a point of a space or a collection of them."
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

    __function: Callable[
        [Union[Point, Collection[Point]]],
        Union[Point, Collection[Point]],
    ]
    __domain: Union[Point, Collection[Point]]
    __codomain: Union[Point, Collection[Point]]
    __param_space: Optional[Space] = None

    @property
    def function(
        self,
    ) -> Callable[[Union[Point, Collection[Point]]], Union[Point, Collection[Point]]]:
        """Get the function of the block."""
        return self.__function

    @property
    def domain(self) -> Union[Point, Collection[Point]]:
        """Get the domains of the block."""
        return self.__domain

    @property
    def codomains(self) -> Union[Point, Collection[Point]]:
        """Get the codomains of the block."""
        return self.__codomain

    @property
    def codomain_names(self) -> Union[str, List[str]]:
        return self._get_space_names(self.codomains)

    @property
    def domain_names(self) -> Union[str, List[str]]:
        return self._get_space_names(self.domain)

    @staticmethod
    def _get_space_names(points: Union[Point, Collection[Point]]) -> Union[str, List[str]]:
        if isinstance(points, (list, tuple)):
            names = []
            for pt in points:
                space, = pt.__args__  # Point should only have 1 arg
                names.append(space.name())
            return names
        space, = points.__args__  # points is a single Point; Point should only have 1 arg
        return space.name()

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
        str_result += f"has domains: {newline}-> {self.domain},{newline}"
        str_result += f"has codomains: {newline}-> {self.codomains},{newline}"

        if self.param_space:
            str_result += f"has parameter space {self.param_space} "

        return str_result

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.__function(*args, **kwargs)
