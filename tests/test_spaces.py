"""Testing spaces.

This should run as part of the CI/CD pipeline.
"""

import numpy as np

from cadcad.spaces import Dimension, Space


def test_space_creation() -> None:
    """Test creation of spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")

    my_space = Space((dim_a, dim_b), "MySpace")

    assert isinstance(my_space, Space)
