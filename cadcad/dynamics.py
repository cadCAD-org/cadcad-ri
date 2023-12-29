"""Blocks and Dynamics definitions."""

from __future__ import annotations

import itertools
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Collection, List, Optional, Union, get_args

from cadcad.points import Point
from cadcad.spaces import Space


def block(
    func: Callable[
        [Union[Point[Space], Collection[Point[Space]]]],
        Union[Point[Space], Collection[Point[Space]]],
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

    if (
        hasattr(return_type, "__origin__")
        and issubclass(return_type.__origin__, Point)
        and isinstance(specialized_type, Space)
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

    domain_types = list(func_annotations.values())
    specialized_domain = [get_args(dom) for dom in domain_types]
    specialized_domain_types = list(itertools.chain(*specialized_domain))

    domain: List[Point] = []

    for domain_tuple in zip(domain_types, specialized_domain_types):
        if (
            hasattr(domain_tuple[0], "__origin__")
            and issubclass(domain_tuple[0].__origin__, Point)
            and isinstance(domain_tuple[1], Space)
        ):
            domain.append(domain_tuple[0])
        elif (
            isinstance(domain_tuple[0], Collection)
            and isinstance(domain_tuple[1], Point)
            and isinstance(get_args(domain_tuple[1])[0], Space)
        ):
            domain.append(domain_tuple[0])  # type: ignore
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
    def codomain(self) -> Union[Point, Collection[Point]]:
        """Get the codomains of the block."""
        return self.__codomain

    @property
    def codomain_names(self) -> Union[str, List[str]]:
        return self._get_space_names(self.codomain)

    @property
    def domain_names(self) -> Union[str, List[str]]:
        return self._get_space_names(self.domain)

    @staticmethod
    def _get_space_names(points: Union[Point, Collection[Point]]) -> Union[str, List[str]]:
        if isinstance(points, (list, tuple)):
            names = []
            for pt in points:
                (space,) = pt.__args__  # Point should only have 1 arg
                names.append(space.name())
            return names
        (space,) = points.__args__  # points is a single Point; Point should only have 1 arg
        return space.name()

    @property
    def param_space(self) -> Optional[Space]:
        """Get the parameter space of the block."""
        return self.__param_space

    def name(self) -> str:
        """Get the name of the block."""
        return self.__function.__name__

    def is_composable(self, blk: Block) -> bool:
        """_summary_

        Parameters
        ----------
        blk : Block
            _description_

        Returns
        -------
        bool
            _description_
        """
        # TODO: Refactor for other compositions
        return self.codomain == blk.domain[0]

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
        str_result += f"has domain: {newline}-> {self.domain},{newline}"
        str_result += f"has codomain: {newline}-> {self.codomain},{newline}"

        if self.param_space:
            str_result += f"has parameter space {self.param_space} "

        return str_result

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.__function(*args, **kwargs)

############ Built-in Blocks ############

def pass_through(block: Block) -> Block:
    """_summary_

    Parameters
    ----------
    block : Block
        _description_

    Returns
    -------
    Block
        _description_
    """
    if not isinstance(block, Block):
        raise TypeError("The argument must be a block")

    # TODO: Pass through composition of blocks
    def new_function(*args: Any, **kwargs: Any) -> Point[Space] | Collection[Point[Space]]:
        return block.function(*args, **kwargs)

    annotation_dict = deepcopy(block.function.__annotations__)

    new_function.__annotations__.clear()
    new_function.__annotations__.update(annotation_dict)

    return block(new_function)

def cartesian_product(*blocks: Block) -> Block:
    """_summary_

    Parameters
    ----------
    blocks : List[Block]
        _description_

    Returns
    -------
    Block
        _description_
    """
    if not blocks:
        raise ValueError("At least one block must be provided")

    def new_function(*args: Any, **kwargs: Any) -> Point[Space] | Collection[Point[Space]]:
        return list(itertools.product(*[blk.function(*args, **kwargs) for blk in blocks]))

    annotation_dict = deepcopy(blocks[0].function.__annotations__)

    new_function.__annotations__.clear()
    new_function.__annotations__.update(annotation_dict)

    return block(new_function)

def decomposition(*blocks: Block) -> Block:
    """_summary_

    Parameters
    ----------
    blocks : List[Block]
        _description_

    Returns
    -------
    Block
        _description_
    """
    if not blocks:
        raise ValueError("At least one block must be provided")

    # TODO: Decomposition of blocks

    annotation_dict = deepcopy(blocks[0].function.__annotations__)

    new_function.__annotations__.clear()
    new_function.__annotations__.update(annotation_dict)

    return block(new_function)

def selection(block: Block, *args: Any, **kwargs: Any) -> Block:
    """_summary_

    Parameters
    ----------
    block : Block
        _description_

    Returns
    -------
    Block
        _description_
    """
    if not isinstance(block, Block):
        raise TypeError("The argument must be a block")

    return block(lambda *args, **kwargs: block.function(*args, **kwargs)[0])

def summation(*blocks: Block) -> Block:
    """_summary_

    Parameters
    ----------
    blocks : List[Block]
        _description_

    Returns
    -------
    Block
        _description_
    """
    if not blocks:
        raise ValueError("At least one block must be provided")

    return block()
