"""Points and Trajectories definitions."""

from typing import Any, Dict
from frozendict import frozendict

from cadcad.spaces import Space
from cadcad.errors import SchemaError


class Point():
    """
    Points in cadCAD.

    Attributes
    ----------
    space: Space
        space which the point must conform to
    data: Dict[str, Any]
        dictionary of dimension names to data that obeys the dimension type
    """

    def __init__(self, space: Space, data: Dict[str, Any]):
        """Build a space based on a tuple of dimensions.

        Args:
            space (Space): space which the point must conform to
            data: (Dict[str, Any]): dict of dimension names to data that obeys the dimension type
        Raises:
            SchemaError: if there is a mismatch between the data and space's schema
        """
        self.__space: Space = space

        internal_data = {}

        for key, value in data.items():
            if key in space.schema.keys() and isinstance(
                    space.schema[key], type) and isinstance(
                        value, space.schema[key]):
                internal_data[key] = value
            else:
                expected_schema = [
                    f"{name} -> {dim.dtype}"
                    for name, dim in space.schema.items()
                ]
                raise SchemaError(space.name, expected_schema,
                                  f"{key} -> {type(value)}")

        self.__data: Dict[str, Any] = frozendict(internal_data)

    @property
    def space(self) -> Space:
        """Get Space of the Point."""
        return self.__space

    def __getitem__(self, key: str) -> Any:
        """Get data inside of the point through indexing."""
        return self.__data[key]

    def __str__(self) -> str:
        """Return a string representation of a point."""
        newline = '\n'
        return f"Frozen point in space {self.space.name} has data{newline}{self.__data}{newline}"
