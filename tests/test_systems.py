from pytest import fixture
import pytest

from cadcad.dynamics import block
from cadcad.errors import BlockInputError, BlockOutputError, WiringError
from cadcad.points import Point
from cadcad.spaces import space
from cadcad.systems import Experiment


@fixture
def first_space():
    @space
    class FirstSpace:
        foo: int
        bar: int

    return FirstSpace


@fixture
def second_space():
    @space
    class SecondSpace:
        pickles: float
        skittles: float

    return SecondSpace


@fixture
def third_space():
    @space
    class ThirdSpace:
        candy: str
        popcorn: str

    return ThirdSpace


@fixture
def first_block(first_space, second_space):
    @block
    def first_space_to_second_space(domain: Point[first_space]) -> Point[second_space]:
        return Point(
            second_space,
            {
                "pickles": 1.,
                "skittles": 2.
            }
        )
    return first_space_to_second_space


@fixture
def second_block(second_space, third_space):
    @block
    def second_space_to_third_space(domain: Point[second_space]) -> Point[third_space]:
        return Point(
            third_space,
            {
                "candy": "yum",
                "popcorn": "ew"
            }
        )
    return second_space_to_third_space


@fixture
def first_block_with_invalid_output(first_space, second_space, third_space):
    @block
    def first_space_to_second_space(domain: Point[first_space]) -> Point[second_space]:
        return Point(
            third_space,
            {
                "candy": "yum",
                "popcorn": "ew"
            }
        )
    return first_space_to_second_space


@fixture(scope="module")
def experiment_params():
    return {"iteration_n": 1, "steps": 1}


def test_valid_wiring(first_block, second_block, experiment_params):
    Experiment(None, experiment_params, (first_block, second_block))


def test_invalid_wiring(first_block, experiment_params):
    with pytest.raises(WiringError) as e:
        Experiment(None, experiment_params, (first_block, first_block))
    assert e.value.message == "Block (first_space_to_second_space) codomain (SecondSpace) does not *exactly match* subsequent block (first_space_to_second_space) domain (FirstSpace)."


def test_valid_block_input(first_space, first_block, experiment_params):
    init_state = Point(first_space, {"foo": 1, "bar": 2})
    Experiment(init_state, experiment_params, (first_block,)).run()


def test_invalid_block_input(second_space, first_block, experiment_params):
    init_state = Point(second_space, {"pickles": 1., "skittles": 2.})
    with pytest.raises(BlockInputError) as e:
        Experiment(init_state, experiment_params, (first_block,)).run()
    assert e.value.message == "Block first_space_to_second_space requires Point[FirstSpace] as input; you passed Point[SecondSpace]"


def test_valid_block_output(first_space, first_block, experiment_params):
    init_state = Point(first_space, {"foo": 1, "bar": 2})
    Experiment(init_state, experiment_params, (first_block,)).run()


def test_invalid_block_output(first_space, first_block_with_invalid_output, experiment_params):
    init_state = Point(first_space, {"foo": 1, "bar": 2})
    with pytest.raises(BlockOutputError) as e:
        Experiment(init_state, experiment_params, (first_block_with_invalid_output,)).run()
    assert e.value.message == "Block first_space_to_second_space must return Point[SecondSpace]; returned Point[ThirdSpace] instead"