"""Testing points.

This should run as part of the CI/CD pipeline.
"""

import pytest

from cadcad.spaces import Space
from cadcad.trajectories import Point
from cadcad.errors import SchemaError


def test_point_creation() -> None:
    """Test creation of points."""
    my_space = Space({'age': int}, "MySpace")

    my_data = {"age": 29}

    my_point = Point(my_space, my_data)

    assert isinstance(my_point, Point)
    assert my_point.space == my_space
    assert my_point["age"] == 29


def test_point_creation_nested_space() -> None:
    """Test creation of points with nested spaces."""
    my_space = Space({'age': int}, "MySpace")

    my_data = {"age": 29}

    my_point = Point(my_space, my_data)

    assert isinstance(my_point, Point)
    assert my_point.space == my_space
    assert my_point["age"] == 29


def test_point_creation_wrong_schema() -> None:
    """Test creation of points with the wrong schema."""
    my_space = Space({'age': int}, "MySpace")

    with pytest.raises(SchemaError):
        _ = Point(my_space, {"age": "29"})

    with pytest.raises(SchemaError):
        _ = Point(my_space, {"ag": 29})


def test_point_printing() -> None:
    """Test printing of points."""
    my_space = Space({'age': int}, "MySpace")

    my_point = Point(my_space, {"age": 29})

    assert str(
        my_point) == 'Frozen point in space MySpace has data\n{\n    "age": 29\n}\n'
