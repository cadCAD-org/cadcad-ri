"""State testing.

TODO: Create more comprehensive testing
"""
from __future__ import annotations
from dataclasses import dataclass

from cadcad.state import MetaState


@dataclass(frozen=True, repr=False)
class State(MetaState):
    """Class to store information about the state of the simulation.

    Inherits from:
        MetaState (Abstract Base Dataclass): The blueprint necessary for a State class

    Inherited atributes:
        timestep (int): Timestep when the state was created
        substep (int): Substep when the state was created
    """

    prey_population: int
    predator_population: int


def test_class_creation() -> None:
    """Test class creation."""
    prey_predator = State(prey_population=15,
                          predator_population=20,
                          timestep=0,
                          substep=0)
    print(prey_predator)

    assert isinstance(prey_predator, MetaState)
