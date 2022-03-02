"""Testing dimensions.

This should run as part of the CI/CD pipeline.
"""

import pytest
import numpy as np

from cadcad.spaces import Dimension
from cadcad.errors import FreezingError


def test_dim_creation() -> None:
    """Test creation of dimensions."""
    dim_a = Dimension(str, "a")

    assert isinstance(dim_a, Dimension)


def test_dim_print() -> None:
    """Test printing of dimensions."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(int, "b", "Desc B")
    dim_c = Dimension(float, "c", "Desc C", True)
    dim_d = Dimension(int, "d", _frozen=True)

    assert str(
        dim_a
    ) == "Mutable dimension a has data type <class 'str'> and no description"

    assert str(
        dim_b
    ) == "Mutable dimension b has data type <class 'int'> and the following description:\nDesc B\n"

    assert str(
        dim_c
    ) == "Frozen dimension c has data type <class 'float'> and the following description:\nDesc C\n"

    assert str(
        dim_d
    ) == "Frozen dimension d has data type <class 'int'> and no description"


def test_dim_get_set() -> None:
    """Test getters and setters of dimensions."""
    dim_a = Dimension(str, "a")
    dim_b = Dimension(int, "b", "Description of B")
    dim_c = Dimension(float, "c", "Description of C", True)
    dim_d = Dimension(int, "d", _frozen=True)

    assert dim_b.name == "b"
    assert dim_a.description == ""
    assert dim_c.description == "Description of C"
    assert dim_d.dtype == int

    assert not dim_a.is_frozen()
    assert not dim_b.is_frozen()
    assert dim_c.is_frozen()
    assert dim_d.is_frozen()

    dim_a.name = "New Name A"
    assert dim_a.name == "New Name A"

    dim_a.description = "New Description A"
    assert dim_a.description == "New Description A"

    dim_b.dtype = str
    assert dim_b.dtype == str

    dim_a.freeze()
    assert dim_a.is_frozen()


def test_dim_freezing() -> None:
    """Test the freezing of dimensions."""
    dim_c = Dimension(float, "c", "Description of C", True)

    with pytest.raises(FreezingError):
        dim_c.name = "New Name C"

    with pytest.raises(FreezingError):
        dim_c.description = "New Description C"

    with pytest.raises(FreezingError):
        dim_c.dtype = str


def test_dim_equality() -> None:
    """Test the equality of dimensions."""
    dim_a = Dimension(int, "a")
    dim_b = Dimension(int, "a", "Description")
    dim_c = Dimension(float, "d", "Description", True)
    dim_d = Dimension(float, "d", "Description")
    dim_e = Dimension(int, "e", _frozen=True)
    not_dim = (int, "a")

    assert dim_a != dim_b
    assert dim_c == dim_d
    assert dim_c != dim_e

    with pytest.raises(NotImplementedError):
        assert dim_a == not_dim


def test_dim_creation_exotic() -> None:
    """Test the creation of dimensions with exotic types."""
    # Creation of a dimension with a numpy type
    dim_a = Dimension(np.int64, "a")
    assert isinstance(dim_a, Dimension)

    # Creation of a dimension with a fixed shape:
    # This is done either by using structured datatypes, by subclassing or by composition

    # Numpy Structured Datatypes:
    # https://numpy.org/devdocs/user/basics.rec.html#structured-datatypes

    # First, I create my composite type with the shape I want.
    # np.dtype accepts a list of tuples, one tuple per field.
    # Each tuple has the form (fieldname, datatype, shape) where shape is optional.
    # fieldname is a string and can be an empty one,
    # datatype may be any object convertible to a datatype,
    # and shape is a tuple of integers specifying subarray shape.
    my_type = np.dtype([('', float, (2, 2))])
    dim_b = Dimension(my_type, "a")
    assert isinstance(dim_b, Dimension)

    # This works because Python is a dynamic language and there is no runtime enforcing of types,
    # but this fails on mypy.
    # If you want to appease the gods of static analysis, you can subclass np.ndarray or
    # create a new class by composition.


def test_dim_equivalence() -> None:
    """Test the equivalence of dimensions."""
    dim_a = Dimension(int, "a")
    dim_b = Dimension(int, "b", "Description of B")
    dim_c = Dimension(float, "a")
    not_dim = (int, "a")

    assert dim_a.is_equivalent(dim_b)
    assert not dim_a.is_equivalent(dim_c)

    with pytest.raises(NotImplementedError):
        assert dim_a.is_equivalent(not_dim)


def test_dim_copy() -> None:
    """Test the copy of dimensions."""
    dim_a = Dimension(int, "a")
    copy1 = dim_a.copy()
    copy2 = dim_a.copy(name="new_name_for_copy")
    copy3 = dim_a.copy(description="new description for the copy")
    copy4 = dim_a.__copy__()

    assert isinstance(copy1, Dimension)
    assert isinstance(copy2, Dimension)
    assert isinstance(copy3, Dimension)
    assert isinstance(copy4, Dimension)

    assert dim_a == copy1
    assert dim_a == copy4
    assert copy2.name == "new_name_for_copy"
    assert copy3.description == "new description for the copy"
    assert dim_a.is_equivalent(copy2)
    assert dim_a.is_equivalent(copy3)
