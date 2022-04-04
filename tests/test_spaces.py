"""Testing spaces.

This should run as part of the CI/CD pipeline.
"""
from copy import copy as cp
from copy import deepcopy as dcp

import pytest
import numpy as np

from cadcad.spaces import Space
from cadcad.errors import FreezingError, CopyError


def test_space_creation() -> None:
    """Test creation of spaces."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")
    my_space2 = Space(
        {
            'a': {
                'inner_a': np.double,
                'another_inner_a': int
            },
            'b': np.double,
            'c': {
                'inner_c': float
            }
        }, "MySpace2", "My space description", True)

    my_space.description = "A description for MySpace"

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Space({'a': 34, 'b': np.double}, "My Space 4")  # type: ignore

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Space({'a': {'inner_a': 34}, 'b': np.double}, "My Space 4")

    assert isinstance(my_space, Space)
    assert isinstance(my_space2, Space)

    assert my_space.name == "MySpace"
    assert my_space2.description == "My space description"


def test_space_schema_view() -> None:
    """Test the immutable view of space's schemas."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")

    assert my_space.pretty_schema() == '{\n    "a": "<class \'numpy.float64\'>",\n    "b": "<class \'numpy.float64\'>"\n}'  # noqa: E501


def test_space_freezing() -> None:
    """Test the freezing of spaces."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")
    my_space.name = "AnotherName"

    my_space2 = Space({'a': np.double, 'b': int}, "MySpace2", frozen=True)

    with pytest.raises(FreezingError):
        my_space2.description = "Trying to change the description"

    with pytest.raises(FreezingError):
        my_space2.name = "Trying to change the name"

    with pytest.raises(FreezingError):
        my_space2.add_dimensions({'c': int})

    assert not my_space.is_frozen()
    assert my_space2.is_frozen()

    my_space.freeze()

    assert my_space.is_frozen()


def test_add_dims() -> None:
    """Test adding dimensions to spaces."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")

    my_space.add_dimensions({'c': int})

    assert my_space['a'] == np.double
    assert my_space['b'] == np.double
    assert my_space['c'] == int

    with pytest.raises(ValueError):  # noqa: PT011
        my_space.add_dimensions({'a': float})

    assert my_space['a'] != float


def test_subspace_spaces() -> None:
    """Test subspacing from other spaces."""
    # One can subspace frozen or unfrozen spaces
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace", frozen=True)

    new_space = my_space.subspace(("a", ))

    assert new_space.pretty_schema() == '{\n    "a": "<class \'numpy.float64\'>"\n}'

    # Subspaces are always unfrozen
    assert not new_space.is_frozen()

    # Subspacing from an empty sequence returns an empty space
    new_space_2 = my_space.subspace(())
    assert new_space_2.is_empty()


def test_space_copy() -> None:
    """Test copying spaces with the standart functions."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace", frozen=True)

    # It's forbidden to use the copy function from the stdlib
    with pytest.raises(CopyError):
        _ = cp(my_space)

    # It's forbidden to use the deepcopy function from the stdlib
    with pytest.raises(CopyError):
        _ = dcp(my_space)

    new_space = my_space.copy()

    # Copies are always unfrozen
    assert not new_space.is_frozen()


def test_space_equality() -> None:
    """Test equality between spaces and other objects."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace", frozen=True)
    my_space2 = Space({'a': np.double, 'b': np.double}, "MySpace2")

    assert my_space != my_space2

    with pytest.raises(ValueError, match='Impossible to compare'):
        assert my_space == 'string'


def test_space_equivalence() -> None:
    """Test equality between spaces and other objects."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace", frozen=True)
    my_space2 = Space({'a': np.double, 'b': np.double}, "MySpace2")

    assert my_space.is_equivalent(my_space2)

    with pytest.raises(ValueError, match='Impossible to compare'):
        assert my_space.is_equivalent(4)


def test_space_print() -> None:
    """Test printing of spaces."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")
    assert str(my_space) == "Unfrozen space MySpace has dimensions ['a', 'b'] "

    my_space2 = Space({'a': np.double, 'b': np.double}, "MySpace", "Desc")
    assert str(
        my_space2
    ) == "Unfrozen space MySpace has dimensions ['a', 'b'] and description:\nDesc\n"

    my_space3 = Space({'a': np.double, 'b': np.double}, "MySpace", frozen=True)
    assert str(my_space3) == "Frozen space MySpace has dimensions ['a', 'b'] "

    my_space4 = Space({'a': {'inner_a': int}}, "MySpace")
    assert str(my_space4) == "Unfrozen space MySpace has dimensions ['a', 'inner_a'] "


def test_space_mult() -> None:
    """Test cartesian product of spaces."""
    my_space = Space({'a': np.double}, "MySpace", frozen=True)
    other_space = Space({'c': int}, "OtherSpace")

    product1 = my_space * other_space

    assert isinstance(product1, Space)
    assert product1.name == "MySpace x OtherSpace"
    assert not product1.is_frozen()
    assert not product1.is_empty()
    assert product1.pretty_schema() == '{\n    "a": "<class \'numpy.float64\'>",\n    "c": "<class \'int\'>"\n}'  # noqa: E501

    # The empty space is the neutral (or identity) element of the multiplication
    product3 = my_space * Space({}, "EmptySpace")
    assert my_space.is_equivalent(product3)
    assert not product3.is_empty()

    # Dimension collision changes the name of the collided dimension
    collided_space = Space({'a': np.int8}, "Collided")
    with pytest.raises(ValueError, match='Collision of dimension'):
        _ = my_space * collided_space

    with pytest.raises(ValueError, match='Impossible to multiply'):
        my_space *= 4


def test_drop_dim() -> None:
    """Test removing dimensions from spaces by the dimension name."""
    my_space = Space({'a': np.double, 'b': np.double}, "MySpace")

    assert my_space.pretty_schema() == '{\n    "a": "<class \'numpy.float64\'>",\n    "b": "<class \'numpy.float64\'>"\n}'  # noqa: E501

    my_space.drop_dimension("b")

    assert my_space.pretty_schema() == '{\n    "a": "<class \'numpy.float64\'>"\n}'  # noqa: E501

    my_space2 = Space({'a': np.int8}, "MySpace2", frozen=True)

    with pytest.raises(FreezingError):
        my_space2.drop_dimension('a')

    with pytest.raises(KeyError):
        my_space.drop_dimension('c')
