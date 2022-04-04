"""Testing points.

This should run as part of the CI/CD pipeline.
"""

import pytest

from cadcad.spaces import Space
from cadcad.trajectories import Point
from cadcad.errors import SchemaError, FreezingError

# def test_point_creation() -> None:
#     """Test creation of points."""
#     dim_a = Dimension(int, "age", "My age in years")

#     my_space = Space((dim_a, ), "My Space")

#     my_data = {"age": 29}

#     my_point = Point(my_space, my_data)

#     assert isinstance(my_point, Point)
#     assert my_point.space == my_space
#     assert my_point["age"] == 29

# def test_point_creation_wrong_schema() -> None:
#     """Test creation of points with the wrong schema."""
#     dim_a = Dimension(int, "age", "My age in years")

#     my_space = Space((dim_a, ), "My Space")

#     with pytest.raises(SchemaError):
#         _ = Point(my_space, {"age": "29"})

#     with pytest.raises(SchemaError):
#         _ = Point(my_space, {"ag": 29})

# def test_point_freezing() -> None:
#     """Test the freezing of points."""
#     dim_a = Dimension(int, "age", "My age in years")
#     dim_b = Dimension(int, "age_months", "My age in months")

#     my_space = Space((dim_a, ), "My Space")
#     another_space = Space((dim_b, ), "Yet Another Space")

#     my_point = Point(my_space, {"age": 29})

#     with pytest.raises(FreezingError):
#         my_point.space = another_space

#     with pytest.raises(FreezingError):
#         my_point["age"] = 15

#     with pytest.raises(FreezingError):
#         del my_point["age"]

# def test_point_printing() -> None:
#     """Test printing of points."""
#     dim_a = Dimension(int, "age", "My age in years")

#     my_space = Space((dim_a, ), "My Space")

#     my_point = Point(my_space, {"age": 29})

#     assert str(
#         my_point) == "Frozen point in space My Space has data\n{'age': 29}\n"
