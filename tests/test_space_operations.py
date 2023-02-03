"""Testing the new space.

This should run as part of the CI/CD pipeline.
"""

from cadcad.spaces import Integer, space


@space
class Space1:
    d_1: Integer
    d_2: Integer


@space
class Space2:
    d_3: Integer
    d_4: Integer


def test_cartesian_product():
    # Test Commutative Properties
    space3 = Space1 * Space2
    space4 = Space2 * Space1
    assert space3.unroll_schema() == space4.unroll_schema()
    assert len(space3.dimensions()) == len(space4.dimensions())
    assert len(space3.dimensions()) == 2


def test_merge_product():
    # Test Commutative Properties
    space3 = Space1 + Space2
    space4 = Space2 + Space1
    assert space3.unroll_schema() == space4.unroll_schema()
    assert len(space3.dimensions()) == len(space4.dimensions())
    assert len(space3.dimensions()) == (len(Space1.dimensions()) + len(Space2.dimensions()))


def test_repeated_merge_product():
    # num = 5
    # space_1_n = Space1**num
    # assert len(space_1_n.dimensions()) == num
    # for dim_name, dim_type in space_1_n.dimensions().items():
    #     assert "space_1" in dim_name
    #     assert dim_type == Space1.__name__
    pass
