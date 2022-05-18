"""Reimplementation of Spaces as a class factory"""

import logging
import sys
from typing import Any, Union, get_type_hints

from cadcad.errors import IllFormedError, InstanceError

log = logging.getLogger(__name__)


class MetaSpace(type):
    """_summary_

    Parameters
    ----------
    type : _type_
        _description_
    """

    def __str__(cls: type) -> str:
        return f"Space {cls.__name__} has dimensions {cls.dimensions()}"

    def __mul__(cls: type, other: type) -> type:
        return cls.cartesian(other)


# Add metrics, constraints and projections
def space(cls: type) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_

    Returns
    -------
    type
        _description_
    """
    if not get_type_hints(cls):
        raise IllFormedError

    cls.dimensions = classmethod(__dimensions)  # type: ignore
    cls.cartesian = classmethod(__cartesian)  # type: ignore

    setattr(cls, __init__.__name__, __init__)

    class NewSpace(cls, metaclass=MetaSpace):
        """Fake class to enable overloading operators on types"""

    NewSpace.__name__ = cls.__name__

    return NewSpace


def __dimensions(cls: type, as_types: bool = False) -> dict[str, Union[type, str]]:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_

    Returns
    -------
    Dict[str, type]
        _description_
    """
    hints = get_type_hints(cls)

    for key, value in hints.items():
        if str(value)[0] == "<":
            str_value = str(value).split()[1][1:-2]
            if as_types:
                hints[key] = eval(
                    str_value, sys.modules[cls.__module__].__dict__, dict(vars(cls))
                )
            else:
                hints[key] = str_value

    return hints


def __cartesian(cls: type, other: type) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_
    name : str
        _description_
    other : type
        _description_

    Returns
    -------
    type
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    cls_dims = __dimensions(cls, True)
    other_dims = __dimensions(other, True)

    counter = 1
    for key, value in other_dims.items():
        if key in cls_dims.keys():
            log.warning(
                "Collision of dimensions detected. Automatically renaming them..."
            )
            new_key = f"{key}_{other.__name__}_{counter}"
            cls_dims[new_key] = value
        else:
            cls_dims[key] = value

        counter += 1

    new_space = type(
        f"{cls.__name__}x{other.__name__}", cls.__bases__, dict(cls.__dict__)
    )
    setattr(new_space, "__annotations__", cls_dims)

    return space(new_space)


def __init__(self: Any, *args: Any, **kwargs: Any) -> None:  # noqa: N807
    raise InstanceError
