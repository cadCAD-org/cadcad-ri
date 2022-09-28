"""Testing the new space.

This should run as part of the CI/CD pipeline.
"""
from pytest import fixture
from cadcad.spaces import space, Integer


@fixture
def space_1():
    @space
    class Space_1:
        d_1: Integer
        d_2: Integer

    return Space_1


@fixture
def space_2():
    @space
    class Space_2:
        d_3: Integer
        d_4: Integer

    return Space_2


def test_cartesian_product(space_1, space_2):
    # Test Commutative Properties
    Space_3 = space_1 * space_2
    Space_4 = space_2 * space_1
    assert Space_3.unroll_schema() == Space_4.unroll_schema()
    assert len(Space_3.dimensions()) == len(Space_4.dimensions())
    assert len(Space_3.dimensions()) == 2


def test_merge_product(space_1, space_2):
    # Test Commutative Properties
    Space_3 = space_1 + space_2
    Space_4 = space_2 + space_1
    assert Space_3.unroll_schema() == Space_4.unroll_schema()
    assert len(Space_3.dimensions()) == len(Space_4.dimensions())
    assert len(Space_3.dimensions()) == (len(space_1.dimensions()) + len(space_2.dimensions()))


def test_repeated_merge_product(space_1):
    N = 5
    Space_1_N = space_1 ** N
    assert len(Space_1_N.dimensions()) == N
    for dim_name, dim_type in Space_1_N.dimensions().items():
        assert 'space_1' in dim_name
        assert dim_type == space_1.__name__


def test_copy(space_1):
    Space_1_Copy = space_1.copy()
    assert Space_1_Copy.is_equivalent(space_1) and (Space_1_Copy != space_1)