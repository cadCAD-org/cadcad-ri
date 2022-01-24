"""
MetaState definition.

MetaState is an abstract class that provides a blueprint for all statespaces in cadCAD.

[TODO: Document the usage]
"""
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, fields


@dataclass(frozen=True, repr=False)
class MetaState(ABC):
    """
    Blueprint for all statespaces in cadCAD.

    All statespaces must inherit this class and implement its methods.
    """

    timestep: int
    substep: int

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        newline = '\n'
        attributes = ''.join(
            f"{field.name}: {getattr(self, field.name)}{newline}"
            for field in fields(self))

        return f"State at timestep {self.timestep} has attributes: {newline}{attributes}{newline}"
