import pytest
from pytest import fixture

from cadcad.dynamics import Block, block
from cadcad.errors import BlockInputError, BlockOutputError, WiringError
from cadcad.points import Point
from cadcad.spaces import Space, space
from cadcad.systems import Experiment

# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, invalid-name, redefined-outer-name  # noqa: E501


@fixture
def first_space() -> type:
    @space
    class FirstSpace:
        dim1: int
        dim2: int

    return FirstSpace


@fixture
def second_space() -> type:
    @space
    class SecondSpace:
        pickles: float
        skittles: float

    return SecondSpace


@fixture
def third_space() -> type:
    @space
    class ThirdSpace:
        candy: str
        popcorn: str

    return ThirdSpace


@fixture
def first_block(first_space: Space, second_space: Space) -> Block:
    @block
    def first_space_to_second_space(domain: Point[first_space]) -> Point[second_space]:
        return Point(second_space, {"pickles": 1.0, "skittles": 2.0})

    return first_space_to_second_space


@fixture
def second_block(second_space: Space, third_space: Space) -> Block:
    @block
    def second_space_to_third_space(domain: Point[second_space]) -> Point[third_space]:
        return Point(third_space, {"candy": "yum", "popcorn": "ew"})

    return second_space_to_third_space


@fixture
def first_block_with_invalid_output(
    first_space: Space, second_space: Space, third_space: Space
) -> Block:
    @block
    def first_space_to_second_space(domain: Point[first_space]) -> Point[second_space]:
        return Point(third_space, {"candy": "yum", "popcorn": "ew"})

    return first_space_to_second_space


@fixture(scope="module")
def experiment_params() -> dict:
    return {"iteration_n": 1, "steps": 1}


def test_valid_wiring(first_block: Block, second_block: Block, experiment_params: dict) -> None:
    Experiment(None, experiment_params, (first_block, second_block))


def test_invalid_wiring(first_block: Block, experiment_params: dict) -> None:
    with pytest.raises(WiringError) as e:
        Experiment(None, experiment_params, (first_block, first_block))
    assert (
        e.value.message
        == "Block (first_space_to_second_space) codomain (SecondSpace) does not *exactly match* subsequent block (first_space_to_second_space) domain (FirstSpace)."  # noqa: E501
    )


def test_valid_block_input(first_space: Space, first_block: Block, experiment_params: dict) -> None:
    init_state = Point(first_space, {"dim1": 1, "dim2": 2})
    Experiment(init_state, experiment_params, (first_block,)).run()


def test_invalid_block_input(
    second_space: Space, first_block: Block, experiment_params: dict
) -> None:
    init_state = Point(second_space, {"pickles": 1.0, "skittles": 2.0})
    with pytest.raises(BlockInputError) as e:
        Experiment(init_state, experiment_params, (first_block,)).run()
    assert (
        e.value.message
        == "Block first_space_to_second_space requires Point[FirstSpace] as input; you passed Point[SecondSpace]"  # noqa: E501
    )


def test_valid_block_output(
    first_space: Space, first_block: Block, experiment_params: dict
) -> None:
    init_state = Point(first_space, {"dim1": 1, "dim2": 2})
    Experiment(init_state, experiment_params, (first_block,)).run()


def test_invalid_block_output(
    first_space: Space, first_block_with_invalid_output: Block, experiment_params: dict
) -> None:
    init_state = Point(first_space, {"dim1": 1, "dim2": 2})
    with pytest.raises(BlockOutputError) as e:
        Experiment(init_state, experiment_params, (first_block_with_invalid_output,)).run()
    assert (
        e.value.message
        == "Block first_space_to_second_space must return Point[SecondSpace]; returned Point[ThirdSpace] instead"  # noqa: E501
    )
