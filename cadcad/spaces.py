"""Definition of Spaces"""

import logging
from copy import deepcopy
from typing import Any, Dict, Generator, List, Union, get_type_hints

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
        """A space has both a name and an identifier. This methods prints the name."""
        if not cls.dimensions():  # type: ignore
            return f"Empty space {cls.__name__}"

        return f"Space {cls.__name__} has dimensions {cls.dimensions()}"  # type: ignore

    def __mul__(cls: type, other: type) -> type:
        return cls.cartesian(other)  # type: ignore

    def __pow__(cls: type, dimension_n: int) -> type:
        return cls.pow(dimension_n)  # type: ignore

    def __add__(cls: type, other: type) -> type:
        return cls.add(other)  # type: ignore


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
    for value in cls.__annotations__.values():
        if not isinstance(value, type):
            raise IllFormedError

    cls.dimensions = classmethod(__dimensions)  # type: ignore
    cls.cartesian = classmethod(__cartesian)  # type: ignore
    cls.pow = classmethod(__power)  # type: ignore
    cls.name = classmethod(__name)  # type: ignore
    cls.copy = classmethod(__copy)  # type: ignore
    cls.rename_dims = classmethod(__rename_dims)  # type: ignore
    cls.is_empty = classmethod(__is_empty)  # type: ignore
    cls.unroll_schema = classmethod(__unroll_schema)  # type: ignore
    cls.add = classmethod(__add)  # type: ignore
    cls.nest = classmethod(__nest)  # type: ignore

    setattr(cls, __init__.__name__, __init__)

    class NewSpace(cls, metaclass=MetaSpace):
        """Fake class to enable overloading operators on types"""

    NewSpace.__name__ = cls.__name__
    setattr(NewSpace, "__annotations__", cls.__annotations__)

    return NewSpace


def multiply(operands: List[type]) -> type:
    """_summary_

    Parameters
    ----------
    operands : List[MetaSpace]
        _description_

    Returns
    -------
    type
        _description_
    """
    new_space = __copy(EmptySpace)
    new_space.__name__ = "x".join([f"{cls.__name__}" for cls in operands])

    new_annotation = {
        f"{cls.__name__.lower()}_{i}": deepcopy(cls) for i, cls in enumerate(operands)
    }

    setattr(new_space, "__annotations__", new_annotation)

    return new_space


def __dimensions(cls: type, as_types: bool = False) -> Dict[str, Union[type, str]]:
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

    if not as_types:
        for key, value in hints.items():
            hints[key] = value.__name__

    return hints


def __unroll_schema(cls: type) -> Dict[str, Union[dict, str]]:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_

    Returns
    -------
    Dict[str, Union[dict, type]]
        _description_
    """
    dims = __dimensions(cls, as_types=True)
    dims_str = __dimensions(cls)

    for key, value in dims.items():
        if isinstance(value, MetaSpace):
            dims_str[key] = __unroll_schema(value)  # type: ignore

    return dims_str  # type: ignore


def __rename_dims(cls: type, rename_dict: Dict[str, str]) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_
    rename_dict : Dict[str, str]
        _description_

    Returns
    -------
    type
        _description_
    """
    new_space = __copy(cls)
    schema = __dimensions(new_space, as_types=True)

    for old_key, new_key in rename_dict.items():
        if new_key in schema:
            raise KeyError(f"The dimension {new_key} already exists in {cls.__name__}")

        try:
            schema[new_key] = schema.pop(old_key)
        except KeyError as err:
            log.error("Impossible to rename. Dimension %s not found.", old_key)
            raise err

    new_space.__annotations__.clear()

    setattr(new_space, "__annotations__", schema)

    return new_space


def __copy(cls: type) -> type:
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
    cls_dict = deepcopy(dict(cls.__dict__))
    new_space = type(cls.__name__, (object,), cls_dict)
    return space(new_space)


def __name(cls: type) -> str:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_

    Returns
    -------
    str
        _description_
    """
    return cls.__name__


def __cartesian(cls: type, other: type) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_
    other : type
        _description_

    Returns
    -------
    type
        _description_
    """
    if not isinstance(other, MetaSpace):
        raise TypeError("The left hand operand must be a Space")

    if __is_empty(other):
        return cls

    new_space = __copy(cls)
    new_space.__annotations__.clear()

    if cls.__name__ == other.__name__:
        new_space.__annotations__ = {
            f"{cls.__name__.lower()}_0": deepcopy(cls),
            f"{other.__name__.lower()}_1": other,
        }
    else:
        new_space.__annotations__ = {
            cls.__name__.lower(): deepcopy(cls),
            other.__name__.lower(): other,
        }

    new_space.__name__ = f"{cls.__name__}*{other.__name__}"

    return new_space


def __power(cls: type, dimension_n: int) -> type:
    """_summary_
    NOTE: The power of a space is not the repeating cartesian product of a space by itself!

    Parameters
    ----------
    cls : type
        _description_
    dimension_n : int
        _description_

    Returns
    -------
    type
        _description_

    Raises
    ------
    TypeError
        _description_
    """
    if isinstance(dimension_n, int) and dimension_n == 0:
        return EmptySpace

    if isinstance(dimension_n, int) and dimension_n == 1:
        return cls

    if isinstance(dimension_n, int) and dimension_n > 1:
        new_annotation = {
            f"{cls.__name__.lower()}_{i}": deepcopy(cls) for i in range(dimension_n)
        }
        new_space = type(f"{dimension_n}-{cls.__name__}", (object,), dict(cls.__dict__))
        setattr(new_space, "__annotations__", new_annotation)

        return space(new_space)

    raise TypeError("The left hand operand must be a positive integer")


def __add(cls: type, other: type) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_
    other : type
        _description_

    Returns
    -------
    type
        _description_
    """
    if not isinstance(other, MetaSpace):
        raise TypeError("The left hand operand must be a Space")

    if __is_empty(other):
        return cls

    other_dims = __dimensions(other, as_types=True)

    new_space = __copy(cls)
    new_space.__name__ = f"{cls.__name__}+{other.__name__}"

    for dim_name, dim_type in other_dims.items():
        if dim_name in new_space.__annotations__:
            for new_key in __generate_key(dim_name):
                if new_key not in new_space.__annotations__:
                    new_space.__annotations__[new_key] = dim_type
                    break
        else:
            new_space.__annotations__[dim_name] = dim_type

    return space(new_space)


def __nest(cls: type, name_change: bool = True) -> type:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_
    name_change : bool, optional
        _description_, by default True

    Returns
    -------
    type
        _description_
    """
    new_space = __copy(cls)

    if name_change:
        new_space.__name__ = f"nested-{cls.__name__}"

    new_space.__annotations__.clear()
    new_space.__annotations__[cls.__name__] = deepcopy(cls)

    return space(new_space)


def __is_empty(cls: type) -> bool:
    """_summary_

    Parameters
    ----------
    cls : type
        _description_

    Returns
    -------
    bool
        _description_
    """
    return not bool(__dimensions(cls, as_types=True))


def __init__(self: Any, *args: Any, **kwargs: Any) -> None:  # noqa: N807
    raise InstanceError


def __generate_key(existing_key: str) -> Generator:
    """_summary_

    Parameters
    ----------
    existing_key : str
        _description_

    Yields
    ------
    Generator
        _description_
    """
    num = 1
    while True:
        yield f"{existing_key}_{num}"
        num += 1


@space
class EmptySpace:
    """A space with no dimensions.
    It is the multiplicative identity in the algebra of spaces."""


@space
class Real:
    """The one dimensional space of real numbers."""

    real: float


@space
class Integer:
    """The one dimensional space of integer numbers."""

    integer: int


@space
class Bit:
    """The one dimensional space of bits."""

    bit: bool
