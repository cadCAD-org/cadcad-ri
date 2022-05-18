"""Testing the new space.

This should run as part of the CI/CD pipeline.
"""

import pytest

from cadcad.errors import InstanceError
from cadcad.new_space import space


def test_space_creation() -> None:
    """Test creation of spaces."""
    print()

    @space
    class Real:
        value: float

    @space
    class Integer:
        value: int

    MySpace = Real.cartesian(Integer)
    MySpaceMul = Real * Integer

    print(Real)
    print(type(Real))

    print()

    print(MySpace)
    print(type(MySpace))

    print()

    print(MySpaceMul)
    print(type(MySpaceMul))


# @space
# class Real:
#     value: float

#     def sum():
#         pass


# @space
# class Real2:
#     value: Real
#     value2: Real

# @space
# class Real2:
#     value: List[Real]

# Real * Real -> Real^2  # raise warning and rename automatically

# Real.add_dims()
