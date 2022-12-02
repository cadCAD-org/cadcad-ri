"""
Definition of Spaces
"""

import logging
from copy import deepcopy
from typing import Any, Collection, Dict, Generator, Union, get_type_hints

from cadcad.errors import IllFormedError, InstanceError

log = logging.getLogger(__name__)


class Space(type):
    """
    A Space is a container of types, with the property that it contains
    composition operators, allowing one Space to be composed of Multiple Spaces
    as an input.
    """

    def __str__(cls: type) -> str:
        """
        A space has both a name and an identifier. This methods prints the name.
        """
        if not cls.dimensions():  # type: ignore
            return f"Empty space {cls.__name__}"
        else:
            return f"Space {cls.__name__} has dimensions {cls.dimensions()}"  # type: ignore

    def __repr__(cls) -> str:
        """
        A space has both a name and an identifier. This methods prints the name.
        """
        if not cls.dimensions():  # type: ignore
            return f"Empty space {cls.__name__}"
        else:
            return f"Space {cls.__name__} has dimensions {cls.dimensions()}"  # type: ignore

    def __mul__(cls: type, other: type) -> type:
        return cls.cartesian(other)  # type: ignore

    def __pow__(cls: type, dimension_n: int) -> type:
        return cls.pow(dimension_n)  # type: ignore

    def __add__(cls: type, other: type) -> type:
        return cls.add(other)  # type: ignore


# Add metrics, constraints and projections
def space(cls: type) -> type:
    """
    Decorator for generating a new Space type from a class definition that follows the Space semantics - i.e. dimensions are type-annotated member variables with undefined values.

    Parameters
    ----------
    cls : type
        Space definition as a class, on which dimensions as type-annotated member variables with undefined values.


    Returns
    -------
    type
        a Space type.
    """

    # Fix a bug on some environments where the annotations field does not exists.
    if not hasattr(cls, '__annotations__'):
        setattr(cls, '__annotations__', {})


    for value in cls.__annotations__.values():
        if not isinstance(value, type):
            raise IllFormedError

    # Instance methods for the Space type.
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
    cls.is_equivalent = classmethod(__is_equivalent)  # type: ignore

    setattr(cls, __init__.__name__, __init__)

    class NewSpace(cls, metaclass=Space):
        """
        Fake class to enable overloading operators on types
        """

    NewSpace.__name__ = cls.__name__
    setattr(NewSpace, "__annotations__", cls.__annotations__)

    return NewSpace


def multiply(operands: Collection[type]) -> type:
    """
    Compose multiple spaces into a single space.

    Parameters
    ----------
    operands : List[Space]
        Spaces to be concatenated together.

    Returns
    -------
    type
        A new space on which dimensions are the union of the input spaces. The names follows an ordinal order.
    """
    new_space = __copy(EmptySpace)
    new_space.__name__ = "x".join([f"{cls.__name__}" for cls in operands])

    new_annotation = {
        f"{cls.__name__.lower()}_{i}": deepcopy(cls)
        for i, cls
         in enumerate(operands)
    }

    setattr(new_space, "__annotations__", new_annotation)

    return new_space


def __dimensions(cls: type, as_types: bool = False) -> Dict[str, Union[type, str]]:
    """
    Return a dictionary of the dimensions of a Space type where keys are names
    and values are types.

    Parameters
    ----------
    cls : type
        Space type to retrieve dimensions.

    Returns
    -------
    Dict[str, type]
        Keys are names of dimensions and values are types.
    """
    hints = get_type_hints(cls)

    # If there are class type hints, then set `hints` to be the an map
    # key is the name and value is the type.
    if not as_types:
        for variable_name, variable_type in hints.items():
            hints[variable_name] = variable_type.__name__

    return hints


def __unroll_schema(cls: type) -> Dict[str, Union[dict, str]]:
    """
    Extract a Dictionary schema of the Space dimensions. It is recursive if there are dimensions which are also Space.

    Parameters
    ----------
    cls : type
        Space to be unrolled.

    Returns
    -------
    Dict[str, Union[dict, type]]
        A dict schema of the dimensions. Nested if there are inner Spaces.
    """
    dims = __dimensions(cls, as_types=True)
    dims_str = __dimensions(cls)

    for key, value in dims.items():
        if isinstance(value, Space):
            dims_str[key] = __unroll_schema(value)  # type: ignore

    return dims_str  # type: ignore


def __rename_dims(cls: type, rename_dict: Dict[str, str]) -> type:
    """
    Parameters
    ----------
    cls : type
        Space on which to rename dimensions
    rename_dict : Dict[str, str]
        Map on which keys are old names and values are new names.

    Returns
    -------
    type
        Space with renamed dimensions.
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
    """
    Perform an deepcopy over an given space.

    Parameters
    ----------
    cls : type
        Space to be copied.

    Returns
    -------
    type
        New space instance.
    """
    cls_dict = deepcopy(dict(cls.__dict__))
    new_space = type(cls.__name__, (object,), cls_dict)
    return space(new_space)


def __name(cls: type) -> str:
    """
    Retrieve the name of a Space type.

    Parameters
    ----------
    cls : type
        Space type.

    Returns
    -------
    str
        Name of the Space type.
    """
    return cls.__name__


def __cartesian(cls: type, other: type) -> type:
    """
    Concatenate two spaces into a single space.

    `Space_1 * Space_2 = Space_3`, where `Space_3` has two dimensions of values
    `Space_1` and `Space_2`.

    Parameters
    ----------
    cls : type
        Space 1 to be concatenated.
    other : type
        Space 2 to be cocnatenated.

    Returns
    -------
    type
        An concatenated space, on which the dimensions are the input spaces.
    """
    if not isinstance(other, Space):
        raise TypeError("The left hand operand must be a Space")

    if __is_empty(other):
        return cls
    elif __is_empty(cls):
        return other

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
    """
    Repeated merge of a space against itself, n times. Eg. `Space_1 ** 4 = Space_1 + Space_1 + Space_1 + Space_1`


    NOTE: The power of a space is not the repeating cartesian product of a space by itself, but rather it is the repeating merge operation.

    Parameters
    ----------
    cls : type
        Space on which to apply the repeated merge operation.
    dimension_n : int
        How many times to merge the space against itself.

    Returns
    -------
    type
        `Space^n`

    Raises
    ------
    TypeError
        Triggered if `dimensions_n` is not an integer and is below 0.
    """
    if isinstance(dimension_n, int) and dimension_n == 0:
        return EmptySpace

    if isinstance(dimension_n, int) and dimension_n == 1:
        return cls

    if isinstance(dimension_n, int) and dimension_n > 1:
        new_annotation = {f"{cls.__name__.lower()}_{i}": deepcopy(cls) for i in range(dimension_n)}
        new_space = type(f"{dimension_n}-{cls.__name__}", (object,), dict(cls.__dict__))
        setattr(new_space, "__annotations__", new_annotation)

        return space(new_space)

    raise TypeError("The left hand operand must be a positive integer")


def __add(cls: type, other: type) -> type:
    """
    Merge two Spaces.

    Eg. `Space_1 + Space_2 = Space_3`, on which the dimensions of `Space_3` is
    the union of the dimensions of `Space_1` and `Space_2`.

    Parameters
    ----------
    cls : type
        Space 1 to be merged.
    other : type
        Space 2 to be merged.

    Returns
    -------
    type
        An merged space, on which the dimensions are the union of the dimensions of the input spaces.
    """
    if not isinstance(other, Space):
        raise TypeError("The left hand operand must be a Space")

    if __is_empty(other):
        return cls
    elif __is_empty(cls):
        return other

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
    """
    Rolls the space dimensions into a new space, which then substitutes the input space dimensions.

    Eg. on `Space_2 = Space_1.nest()`, `Space_2` has an single dimension with the name and value being `Space_1`.

    Parameters
    ----------
    cls : type
        Space to nest.
    name_change : bool, optional
        If True, the name of the new root space will include an `nested-` prefix.

    Returns
    -------
    type
        Nested space.
    """
    new_space = __copy(cls)

    if name_change:
        new_space.__name__ = f"nested-{cls.__name__}"

    new_space.__annotations__.clear()
    new_space.__annotations__[cls.__name__] = deepcopy(cls)

    return space(new_space)


def __is_empty(cls: type) -> bool:
    """
    Checks if an Space has any defined dimensions.

    Parameters
    ----------
    cls : type
        Space to check the dimensions against.

    Returns
    -------
    bool
        True if there are no defined dimensionse, False otherwise.
    """
    return not bool(__dimensions(cls, as_types=True))


def __init__(self: Any, *args: Any, **kwargs: Any) -> None:  # noqa: N807
    raise InstanceError


def __generate_key(existing_key: str) -> Generator[str, None, None]:
    """
    Ordinal number generator for a dimension.

    Parameters
    ----------
    existing_key : str
        Dimension name.

    Yields
    ------
    Generator for the dimension name.

    """
    num = 1
    while True:
        yield f"{existing_key}_{num}"
        num += 1


def __is_equivalent(cls: type, other: type) -> bool:
    """
    Check if two Space types are equivalent in terms of their dimension types.

    Parameters
    ----------
    cls : type
    other : type

    Returns
    -------
    bool
        True if the Space Dimensions are all equal, False otherwise.
    """
    return list(__dimensions(cls, True).values()) == list(__dimensions(other, True).values())


@space
class EmptySpace:
    """
    A space with no dimensions.
    It is the multiplicative identity in the algebra of spaces.
    """


@space
class Real:
    """
    The one dimensional space of real numbers.
    """
    real: float


@space
class Integer:
    """
    The one dimensional space of integer numbers.
    """
    integer: int


@space
class Bit:
    """
    The one dimensional space of bits.
    """

    bit: bool
