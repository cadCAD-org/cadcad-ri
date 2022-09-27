"""Systems, Simulations and Experiments definitions."""

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from cadcad.dynamics import Block
from cadcad.points import Point


class Trajectory:
    """Collection of Points resulting from a simulation"""

    def __init__(self) -> None:
        self.__data: List[Point] = []

    def append(self, new_point: Point) -> None:
        """_summary_

        Parameters
        ----------
        new_point : Point
            _description_
        """
        self.__data.append(new_point)

    @property
    def data(self) -> List[Point]:
        """_summary_

        Returns
        -------
        List[Point]
            _description_
        """
        return self.__data

    def __str__(self) -> str:
        """Return a string representation of a space."""
        newline = "\n"

        str_result = f"Trajectory has points:{newline}"
        for point in self.data:
            str_result += f"{str(point)}{newline}"

        return str_result


@dataclass
class Experiment:
    """Main entrypoint of a cadCAD simulation"""

    init_state: Point
    experiment_params: Dict[str, Any]
    pipeline: Tuple[Block]

    def run(self) -> List[Trajectory]:
        """_summary_

        Returns
        -------
        Trajectory
            _description_
        """
        result_matrix: List[Trajectory] = []

        for _ in range(self.experiment_params["iteration_n"]):
            current_state = self.init_state
            result = Trajectory()
            for _ in range(self.experiment_params["steps"]):
                for block in self.pipeline:
                    next_state = block(current_state)
                    current_state = next_state
                result.append(current_state)

            result_matrix.append(result)

        return result_matrix
