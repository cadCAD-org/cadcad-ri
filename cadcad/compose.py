"""Composition rules definitions."""

from copy import deepcopy
from functools import reduce
from typing import Any, Collection

from cadcad.dynamics import Block, block
from cadcad.points import Point
from cadcad.spaces import Space


def serial_compose(block1: Block, block2: Block) -> Block:
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
    if not isinstance(block1, Block) or not isinstance(block2, Block):
        raise TypeError("The arguments must be blocks")
    if not block1.is_composable(block2):
        raise ValueError("The blocks are not composable")

    def new_function(
        *args: Any, **kwargs: Any
    ) -> Point[Space] | Collection[Point[Space]]:
        return block2.function(block1.function(*args, **kwargs))

    annotation_dict = deepcopy(block1.function.__annotations__)
    annotation_dict["return"] = block2.function.__annotations__["return"]

    new_function.__annotations__.clear()
    # new_function.__annotations__.update(annotation_dict)

    setattr(new_function, "__annotations__", annotation_dict)

    return block(new_function)


def series(*blocks: Block) -> Block:
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
    return block(reduce(lambda f, g: serial_compose(f, g), blocks))


def parallel_compose(block1: Block, block2: Block) -> Block:
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
    if not isinstance(block1, Block) or not isinstance(block2, Block):
        raise TypeError("The arguments must be blocks")

    # TODO: Parallel composition of blocks
    # TODO: Dispatch parallel computation based on spaces
    def new_function(
        *args: Any, **kwargs: Any
    ) -> Point[Space] | Collection[Point[Space]]:
        return ...

    annotation_dict = deepcopy(block1.function.__annotations__)
    annotation_dict["return"] = block2.function.__annotations__["return"]

    new_function.__annotations__.clear()

    setattr(new_function, "__annotations__", annotation_dict)

    return block(new_function)


def parallel(*blocks: Block) -> Block:
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
    # TODO: Parallel composition of blocks
    if not blocks:
        raise ValueError("At least one block must be provided")
    return block(reduce(lambda f, g: parallel_compose(f, g), blocks))


def stack_compose(block1: Block, block2: Block) -> Block:
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
    if not isinstance(block1, Block) or not isinstance(block2, Block):
        raise TypeError("The arguments must be blocks")

    # TODO: Stack composition of blocks
    # TODO: Dispatch stack computation based on spaces
    def new_function(
        *args: Any, **kwargs: Any
    ) -> Point[Space] | Collection[Point[Space]]:
        return ...

    annotation_dict = deepcopy(block1.function.__annotations__)
    annotation_dict["return"] = block2.function.__annotations__["return"]

    new_function.__annotations__.clear()

    setattr(new_function, "__annotations__", annotation_dict)

    return block(new_function)


def stack(*blocks: Block) -> Block:
    """_summary_

    Returns
    -------
    Block
        _description_
    """
    # TODO: Stack composition of blocks
    if not blocks:
        raise ValueError("At least one block must be provided")
    return block(reduce(lambda f, g: stack_compose(f, g), blocks))
