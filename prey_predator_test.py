"""End to end testing through a prey predator simulation."""

import numpy as np

from cadcad.dynamics import block
from cadcad.points import Point
from cadcad.spaces import space
from cadcad.systems import Experiment


@space
class Savanah:
    """Declaration of the types that comprise our simulation"""

    prey_population: int
    predator_population: int


init_state = Point(Savanah, {"prey_population": 100, "predator_population": 15})

experiment_params = {"iteration_n": 1, "steps": 5}


@block
def change_population(domain: Point[Savanah]) -> Point[Savanah]:
    prey_delta = np.random.randint(-2, 3)
    predator_delta = np.random.randint(-2, 3)

    return Point(
        Savanah,
        {
            "prey_population": 100 + prey_delta,
            "predator_population": 15 + predator_delta,
        },
    )


my_experiment = Experiment(init_state, experiment_params, (change_population,))

results = my_experiment.run()
print(results[0])
