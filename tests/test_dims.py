"""Testing dimensions.

This should run as part of the CI/CD pipeline.
"""

from cadcad.dimensions import Dimension


def test_dim_creation() -> None:
    """Test creation of dimensions."""
    dim_a = Dimension("a", str)
    dim_b = Dimension("b", int)

    assert isinstance(dim_a, Dimension)
    assert isinstance(dim_b, Dimension)
