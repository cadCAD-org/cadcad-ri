"""Testing the new space.

This should run as part of the CI/CD pipeline.
"""
from pytest import fixture

from cadcad.spaces import Integer, Real, Space, space

# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name, redefined-outer-name  # noqa: E501


@fixture
def space1() -> type:
    @space
    class Space1:
        d_1: Integer
        d_2: Integer

    return Space1


@fixture
def space2() -> type:
    @space
    class Space2:
        d_3: Integer
        d_4: Integer

    return Space2


@fixture
def emptyspace() -> type:
    @space
    class EmptySpace:
        pass

    return EmptySpace


def test_cartesian_product(space1: Space, space2: Space) -> None:
    # Test Commutative Properties
    Space_3 = space1 * space2  # noqa: N806
    Space_4 = space2 * space1  # noqa: N806
    assert Space_3.unroll_schema() == Space_4.unroll_schema()
    assert len(Space_3.dimensions()) == len(Space_4.dimensions())
    assert len(Space_3.dimensions()) == 2


def test_merge_product(space1: Space, space2: Space) -> None:
    # Test Commutative Properties
    Space_3 = space1 + space2  # noqa: N806
    Space_4 = space2 + space1  # noqa: N806
    assert Space_3.unroll_schema() == Space_4.unroll_schema()
    assert len(Space_3.dimensions()) == len(Space_4.dimensions())
    assert len(Space_3.dimensions()) == (len(space1.dimensions()) + len(space2.dimensions()))


def test_repeated_merge_product(space1: Space) -> None:
    n = 5
    Space_1_N = space1**n  # noqa: N806
    assert len(Space_1_N.dimensions()) == n
    for dim_name, dim_type in Space_1_N.dimensions().items():
        assert "space1" in dim_name
        assert dim_type == space1.__name__


def test_copy(space1: Space) -> None:
    Space_1_Copy = space1.copy()  # noqa: N806
    assert Space_1_Copy.is_equivalent(space1) and (Space_1_Copy != space1)


def test_is_empty(space1: Space, emptyspace: Space) -> None:
    assert not space1.is_empty()
    assert emptyspace.is_empty()


def test_rename_dims(space1: Space) -> None:
    old_dims = space1.dimensions()
    new_dims = space1.rename_dims({"d_1": "new_name"}).dimensions()
    assert new_dims == {"new_name" if k == "d_1" else k: v for k, v in old_dims.items()}


def test_dimensions() -> None:
    @space
    class MyNewSpace:
        d_1: Integer
        d_2: Integer

    assert MyNewSpace.dimensions() == {"d_1": "Integer", "d_2": "Integer"}


def test_name() -> None:
    @space
    class MyNewSpace:
        d_1: Integer
        d_2: Integer

    assert MyNewSpace.name() == "MyNewSpace"


def test_is_equivalent() -> None:
    @space
    class SomeSpace:
        d_1: Integer
        d_2: Integer

    @space
    class SomeEquivalentSpace:
        foo: Integer
        bar: Integer

    @space
    class SomeNonEquivalentSpace:
        d_1: Integer
        d_2: Real

    assert SomeSpace.is_equivalent(SomeEquivalentSpace)
    assert not SomeSpace.is_equivalent(SomeNonEquivalentSpace)


def test_unroll_schema() -> None:
    @space
    class SomeChildSpace:
        d_1: Integer
        d_2: Real

    @space
    class SomeParentSpace:
        d_1: Integer
        d_2: SomeChildSpace

    expected_schema = {
        "d_1": {"integer": "int"},
        "d_2": {"d_1": {"integer": "int"}, "d_2": {"real": "float"}},
    }

    assert SomeParentSpace.unroll_schema() == expected_schema
