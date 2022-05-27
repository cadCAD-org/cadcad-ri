"""Definition of common spaces that can be reused in any simulation."""

from cadcad.spaces import space


@space
class EmptySpace:
    """A space with no dimensions.
    It is the multiplicative identity in the algebra of spaces."""


@space
class Real:
    """The one dimensional space of real numbers."""

    real: float


@space
class Integer:
    """The one dimensional space of integer numbers."""

    integer: int


@space
class Bit:
    """The one dimensional space of bits."""

    bit: bool
