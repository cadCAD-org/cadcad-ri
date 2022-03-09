"""Points and Trajectories definitions."""

from typing import Any, Dict, Tuple, Union

from cadcad.spaces import Space
from cadcad.errors import SchemaError, FreezingError


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
        self.__data: Dict[str, Any] = {}

        for key, value in data.items():
            if key in space.dimensions.keys() and isinstance(
                    value, space.dimensions[key].dtype):
                self.__data[key] = value
            else:
                expected_schema = [
                    f"{name} -> {dim.dtype}"
                    for name, dim in space.dimensions.items()
                ]
                raise SchemaError(space.name, expected_schema,
                                  f"{key} -> {type(value)}")

    @property
    def space(self) -> Space:
        """Get Space of the Point."""
        return self.__space

    @space.setter
    def space(self, change: Any) -> None:
        """Forbid the setter."""
        raise FreezingError(Point)

    def __getitem__(self, key: str) -> Any:
        """Get data inside of the point through indexing."""
        return self.__data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Forbid the setter."""
        raise FreezingError(Point)

    def __delitem__(self, key: str) -> None:
        """Forbid the deleter."""
        raise FreezingError(Point)

    def __str__(self) -> str:
        """Return a string representation of a point."""
        newline = '\n'
        return f"Frozen point in space {self.space.name} has data{newline}{self.__data}{newline}"


class Trajectory():
    """
    Trajectories in cadCAD.

    Attributes
    ----------
    space: Space
    points: Tuple[Point, ...]
        An ordered collection of Points that satisfy the trajectory space
    """

    def __init__(self, points: Union(Point, Tuple[Point, ...])):
        if type(points).__name__ == 'tuple':
            self.__space = points[0].space
            point_list = []

            for p in points:
                if p.space == self.space:
                    point_list.append(p)

            self.__points = tuple(point_list)
        else:
            self.__space = points.space
            self.__points = (points)
    
    @property
    def space(self) -> Space:
        """Get Space."""
        return self.__space

    @property
    def points(self) -> Tuple(Point, ...):
        """Get Points."""
        return self.__points

    def add_point(self, point: Point):
        """Add a point to the trajectory."""
        self.points.append(point)

    def __str__(self) -> str:
        """Return a string representation of a trajectory."""
        newline = '\n'
        return f"Trajectory has data{newline}{self.__data}{newline}"