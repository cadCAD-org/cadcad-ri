"""Testing the new space.

This should run as part of the CI/CD pipeline.
"""

import pytest

from cadcad.spaces import EmptySpace, Integer, Real

# from cadcad.errors import InstanceError
from cadcad.spaces import space


def test_space_creation() -> None:
    """Test creation of spaces."""



