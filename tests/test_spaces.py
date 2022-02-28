"""Testing spaces.

This should run as part of the CI/CD pipeline.
"""
from copy import copy as cp
from copy import deepcopy as dcp

import pytest
import numpy as np

from cadcad.spaces import Dimension, Space
from cadcad.errors import FreezingError, CopyError


def test_space_creation() -> None:
    """Test creation of spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")
    dim_c = Dimension(np.double, "b")

    my_space = Space((dim_a, dim_b), "MySpace")
    my_space2 = Space((dim_a, dim_b), "My Space 2", "My space description")
    my_space3 = Space((dim_c, dim_b),
                      "My Space 3",
                      dim_names=("new name for c", "new name for b"))

    my_space3.description = "A description for My Space 3"

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Space((dim_c, dim_b), "My Space 4", dim_names=("new_dim_name", ))

    with pytest.raises(ValueError):  # noqa: PT011
        _ = Space((dim_c, dim_b), "My Space 5")

    assert isinstance(my_space, Space)
    assert isinstance(my_space2, Space)
    assert isinstance(my_space3, Space)

    assert my_space.name == "MySpace"
    assert my_space2.description == "My space description"
    assert my_space3.description == "A description for My Space 3"


def test_space_creation_from_dict() -> None:
    """Test creation of spaces from dictionaries."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")

    dim_dict = {"a": dim_a, "b": dim_b}

    my_space = Space.from_dict(dim_dict, "MySpace")

    # The above is equivalent to:
    my_space_2 = Space((dim_a, dim_b), "MySpace")

    assert isinstance(my_space, Space)
    assert my_space.name == "MySpace"
    assert my_space == my_space_2


def test_space_freezing() -> None:
    """Test the freezing of spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")
    dim_c = Dimension(np.double, "c")

    my_space = Space((dim_a, dim_b), "MySpace")
    my_space.name = "AnotherName"

    my_space2 = Space((dim_a, dim_b), "MySpace2", frozen=True)

    with pytest.raises(FreezingError):
        my_space2.description = "Trying to change the description"

    with pytest.raises(FreezingError):
        my_space2.name = "Trying to change the name"

    with pytest.raises(FreezingError):
        my_space2.add_dimension(dim_c)

    assert not my_space.is_frozen()
    assert my_space2.is_frozen()

    my_space.freeze()

    assert my_space.is_frozen()


def test_space_renaming() -> None:
    """Test the renaming of dimension inside spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "a")

    my_space = Space((dim_a, dim_b),
                     "My Space",
                     dim_names=("new name for a", "new name for b"))

    assert dim_a.name == "a"
    assert dim_b.name == "a"
    assert my_space.dimensions["new name for a"] == dim_a
    assert my_space.dimensions["new name for b"] == dim_b


def test_add_dims() -> None:
    """Test adding dimensions to spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")
    dim_c = Dimension(np.double, "c")
    dim_d = Dimension(np.double, "a", "Another dim called a")

    my_space = Space((dim_a, dim_b), "MySpace")

    my_space.add_dimension(dim_c)

    assert my_space.dimensions["a"] == dim_a
    assert my_space.dimensions["b"] == dim_b
    assert my_space.dimensions["c"] == dim_c

    with pytest.raises(ValueError):  # noqa: PT011
        my_space.add_dimension(dim_d)

    assert my_space.dimensions["a"] != dim_d

    my_space.add_dimension(dim_d, "new_name_d")

    assert my_space.dimensions["new_name_d"] == dim_d


def test_derive_spaces() -> None:
    """Test deriving spaces from other spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")
    dim_c = Dimension(np.double, "c")

    # One can derive from frozen or unfrozen spaces
    my_space = Space((dim_a, dim_b), "MySpace", frozen=True)

    # One can derive from a tuple of any size
    new_space = my_space.augment((dim_c, ))

    # Deriving from an empty tuple is just a copy
    new_space_2 = my_space.augment(())

    assert isinstance(new_space, Space)
    assert isinstance(new_space_2, Space)

    # Derived spaces are always unfrozen
    assert not new_space.is_frozen()

    # The parent space is independent from the child
    # They don't have the same dimensions, i.e. are not equivalent
    assert not my_space.is_equivalent(new_space)


def test_subspace_spaces() -> None:
    """Test subspacing from other spaces."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")

    # One can subspace frozen or unfrozen spaces
    my_space = Space((dim_a, dim_b), "MySpace", frozen=True)

    new_space = my_space.subspace(("a", ))

    assert list(new_space.dimensions.items()) == [("a", dim_a)]

    # Subspaces are always unfrozen
    assert not new_space.is_frozen()

    # Subspacing from an empty tuple returns an empty space
    new_space_2 = my_space.subspace(())
    assert new_space_2.is_empty()


def test_standart_copy() -> None:
    """Test copying spaces with the standart functions."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")

    my_space = Space((dim_a, dim_b), "MySpace")

    # It's forbidden to use the copy function from the stdlib
    with pytest.raises(CopyError):
        _ = cp(my_space)

    # It's forbidden to use the deepcopy function from the stdlib
    with pytest.raises(CopyError):
        _ = dcp(my_space)


def test_equality_non_space() -> None:
    """Test equality between spaces and other objects."""
    dim_a = Dimension(np.double, "a")
    dim_b = Dimension(np.double, "b")

    my_space = Space((dim_a, dim_b), "MySpace")

    with pytest.raises(NotImplementedError):
        assert my_space == dim_a


def test_space_print() -> None:
    """Test printing of spaces."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(str, "b")

    my_space = Space((dim_a, dim_b), "MySpace")
    assert str(
        my_space
    ) == "Mutable space MySpace has dimensions ('a', 'b') and no description"

    my_space2 = Space((dim_a, dim_b), "MySpace", "Desc")
    assert str(
        my_space2
    ) == "Mutable space MySpace has dimensions ('a', 'b') and the following description:\nDesc\n"

    my_space3 = Space((dim_a, dim_b), "MySpace", frozen=True)
    assert str(
        my_space3
    ) == "Frozen space MySpace has dimensions ('a', 'b') and no description"

    my_space4 = Space((dim_a, dim_b), "MySpace", "Desc", frozen=True)
    assert str(
        my_space4
    ) == "Frozen space MySpace has dimensions ('a', 'b') and the following description:\nDesc\n"


def test_space_mult() -> None:
    """Test cartesian product of spaces."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(str, "b")
    dim_c = Dimension(str, "c")
    dim_d = Dimension(str, "d")

    dims1 = (dim_a, dim_b, dim_c, dim_d)

    my_space = Space((dim_a, dim_b), "MySpace")
    other_space = Space((dim_c, dim_d), "OtherSpace")

    product1 = my_space * other_space

    assert isinstance(product1, Space)
    assert product1.name == "MySpace x OtherSpace"
    assert not product1.is_frozen()
    assert not product1.is_empty()
    assert tuple(product1.dimensions.values()) == dims1

    yet_another_space = Space((dim_d, ), "YASp", frozen=True)
    dims2 = (dim_a, dim_b, dim_d)
    product2 = my_space * yet_another_space
    assert not product2.is_frozen()
    assert not product1.is_empty()
    assert tuple(product2.dimensions.values()) == dims2

    # The empty space is the neutral (or identity) element of the multiplication
    product3 = my_space * Space((), "EmptySpace")
    assert my_space.is_equivalent(product3)
    assert not product3.is_empty()

    # Dimension collision changes the name of the collided dimension
    collided_space = Space((dim_a, ), "Collided")
    product4 = my_space * collided_space
    assert not my_space.is_equivalent(product4)
    assert not product4.is_empty()

    with pytest.raises(NotImplementedError):
        my_space *= 4


def test_index_by_dim_name() -> None:
    """Test indexing spaces by dimension names."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(str, "b")

    my_space = Space((dim_a, dim_b), "MySpace")

    assert my_space["a"] == dim_a
    assert my_space["b"] == dim_b


def test_drop_dim() -> None:
    """Test removing dimensions from spaces by the dimension name."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(str, "b")

    my_space = Space((dim_a, dim_b), "MySpace")
    assert tuple(my_space.dimensions.values()) == (dim_a, dim_b)

    my_space.drop_dimension("b")
    assert tuple(my_space.dimensions.values()) == (dim_a, )
