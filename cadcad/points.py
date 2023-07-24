"""Points and Trajectories definitions."""

import json
from inspect import getmro
from typing import Any, Collection, Dict, Generic, TypeVar, get_args

from cadcad.spaces import EmptySpace, Space

TSpace_co = TypeVar("TSpace_co", bound=Space, covariant=True)

class MetaPoint(type):
    """
    .
    """

    def __str__(cls: type) -> str:
        """
        .
        """
        try:
            if not isinstance(cls.__args__[0], Space):  # type: ignore
                raise TypeError("Points must be specialized by Spaces")
            else:
                return f"Point[{cls.__args__[0].name()}]"  # type: ignore
        except AttributeError:
            raise TypeError("Points must be specialized by Spaces")


    def __repr__(cls) -> str:
        """
        .
        """
        try:
            if not isinstance(cls.__args__[0], Space):  # type: ignore
                raise TypeError("Points must be specialized by Spaces")
            else:
                return f"Point[{cls.__args__[0].name()}]"  # type: ignore
        except AttributeError:
            raise TypeError("Points must be specialized by Spaces")

class Point(Generic[TSpace_co], metaclass=MetaPoint):
    """
    Points in cadCAD.

    Attributes
    ----------
    space: Space
        space which the point must conform to
    data: Dict[str, Any]
        dictionary of dimension names to data that obeys the dimension type
    """

    def __init__(self, space: TSpace_co, data: Dict[str, Any], check_types: bool = True):
        """Build a space based on a tuple of dimensions.

        Args:
            space (Space): space which the point must conform to
            data: (Dict[str, Any]): dict of dimension names to data that obeys the dimension type
        Raises:
            SchemaError: if there is a mismatch between the data and space's schema
        """
        if isinstance(space, Space):
            self.__space = space
        else:
            raise TypeError("Points must be specialized by Spaces")

        dims = space.dimensions(as_types=True)  # type: ignore

        if not isinstance(data, Dict):
            raise TypeError("Point's data must be a dictionary")

        if check_types:
            if check_schema(dims, data):
                self.__data: Dict[str, Any] = data
            else:
                received_type = [f"{name} -> {type(value)}" for name, value in data.items()]
                raise ValueError(
                    "Schema mismatch between the Point's Space and the data given. "
                    + f"Expected {dims}, but received {received_type}"
                )
        else:
            self.__data = data

    @property
    def space(self) -> Space:
        """Get Space of the Point."""
        return self.__space

    @property
    def data(self) -> Dict[str, Any]:
        """Get the data of the Point."""
        return self.__data

    def __getitem__(self, key: str) -> Any:
        """Get data inside of the point through indexing."""
        return self.__data[key]

    def __str__(self) -> str:
        """Return a string representation of a point."""
        newl = "\n"
        data = json.dumps(dict(self.data), indent=4, default=str)
        return f"Point in space {self.space.name()} with data{newl}{data}{newl}"  # type: ignore

    def __repr__(self) -> str:
        """Return a string representation of a point."""
        newl = "\n"
        data = json.dumps(dict(self.data), indent=4, default=str)
        return f"Point in space {self.space.name()} with data{newl}{data}{newl}"  # type: ignore


def check_schema(dim_dict: Dict[str, type], data_dict: Dict[str, Any]) -> bool:
    """_summary_

    Parameters
    ----------
    dim_dict : Dict[str, type]
        _description_
    data_dict : Dict[str, Any]
        _description_

    Returns
    -------
    bool
        _description_
    """
    confirmations = 0

    for (dim_name, dim_type), (data_name, data_value) in zip(
        sorted(dim_dict.items()), sorted(data_dict.items()), strict=True
    ):
        if isinstance(dim_type, type):
            specialized_type = get_args(dim_type)
            dim_mro = getmro(dim_type)
        else:
            raise TypeError("The dimension must be a type.")

        if isinstance(dim_type, Space) and dim_name == data_name:
            inner_dims = dim_type.dimensions(as_types=True)  # type: ignore
            if check_schema(inner_dims, data_value):
                confirmations += 1
        elif dim_name == data_name and specialized_type and issubclass(dim_mro[0], Collection):
            if isinstance(specialized_type[0], Space):
                inner_dims = specialized_type[0].dimensions(as_types=True)  # type: ignore
                if check_schema(inner_dims, data_value[0]):
                    confirmations += 1
            elif isinstance(data_value[0], specialized_type[0]):
                confirmations += 1
        elif dim_name == data_name and not specialized_type and isinstance(data_value, dim_type):
            confirmations += 1

    if confirmations == len(data_dict):
        return True

    return False


empty_point = Point(EmptySpace, {})
