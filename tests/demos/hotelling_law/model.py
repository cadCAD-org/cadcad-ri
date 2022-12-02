from cadcad.spaces import Space
from cadcad.dynamics import Block
import numpy as np
from math import sqrt
from random import choice

from typing import Generator
from dataclasses import dataclass

UP = np.array([0, 1])
DOWN = np.array([0, -1])
LEFT = np.array([1, 0])
RIGHT = np.array([-1, 0])


@dataclass
class Hotels():
    uuid: int
    location: np.ndarray
    price: float


@dataclass
class ConsumerState():
    hotel_grid: np.ndarray
    market_share: dict[int, float]
    revenue: dict[int, float]


@dataclass
class WorldState():
    hotels: list[Hotels]
    market_share: ConsumerState


@dataclass
class WorldParams():
    world_shape: tuple[int, int]


def compute_market_share_grid(n_X: int,
                              n_Y: int,
                              hotels: list[Hotels]) -> np.ndarray:
    hotel_grid = np.zeros([n_X, n_Y])

    # Iterate on each grid point and compute the best hotel using an
    # min(distance * price) criteria.
    for x in range(n_X):
        for y in range(n_Y):
            lower_sum = np.inf
            winner_hotel = None
            for hotel in hotels:
                # Euclidean norm
                dx = x - hotel.location[0]
                dy = y - hotel.location[1]
                distance = sqrt(dx ** 2 + dy ** 2)
                current_sum = distance + hotel.price
                if current_sum < lower_sum:
                    lower_sum = current_sum
                    winner_hotel = hotel.uuid
                elif current_sum == lower_sum:
                    winner_hotel = choice([hotel.uuid, winner_hotel])
                else:
                    pass
            hotel_grid[x, y] = winner_hotel
    return hotel_grid


def compute_market_share(hotel_grid: np.ndarray) -> dict[int, float]:
    uuid_frequency = np.unique(hotel_grid, return_counts=True)
    return dict(zip(*uuid_frequency))


def compute_revenues(hotels: list[Hotels],
                     market_shares: dict[int, float]) -> dict[int, float]:
    return {hotel.uuid: market_shares[hotel.uuid] * hotel.price
            for hotel in hotels}


def realize_consumption(hotels: list[Hotels],
                        world_params: WorldParams) -> ConsumerState:
    n_X = world_params.world_shape[0]
    n_Y = world_params.world_shape[1]

    hotel_grid = compute_market_share_grid(n_X, n_Y, hotels)
    market_shares = compute_market_share(hotel_grid)
    revenues = compute_revenues(hotels, market_shares)

    return ConsumerState(hotel_grid, market_shares, revenues)


def hotel_decisions(world_state: WorldState,
                    world_params: WorldParams) -> list[Hotels]:

    n_X = world_params.world_shape[0]
    n_Y = world_params.world_shape[1]

    new_hotels = world_state.hotels.copy()

    for i, hotel in enumerate(world_state.hotels):
        current_reward = world_state.market_share.revenue[hotel.uuid]

        # Step 1: decide to move or stay
        move = choice([UP, DOWN, LEFT, RIGHT])
        old_location = hotel.location
        new_location = hotel.location + move
        new_location[0] = new_location[0] % n_X
        new_location[1] = new_location[1] % n_Y

        new_hotels[i].location = new_location
        new_world = compute_market_share_grid(n_X, n_Y, new_hotels)
        new_market_share = compute_market_share(new_world)[hotel.uuid]
        new_reward = new_market_share * hotel.price
        if new_reward > current_reward:
            current_reward = new_reward
        else:
            new_hotels[i].location = old_location

        # Step 2: decide to mutate the price
        price_change = choice([-1, 1])
        old_price = hotel.price
        new_price = max(hotel.price + price_change, 0)
        new_hotels[i].price = new_price
        new_world = compute_market_share_grid(n_X, n_Y, new_hotels)
        new_market_share = compute_market_share(new_world)[hotel.uuid]
        new_reward = new_market_share * new_price
        if new_reward > current_reward:
            current_reward = new_reward
        else:
            new_hotels[i].price = old_price
    return new_hotels


@dataclass
class HotellingLawModel():
    hotels: list[Hotels]
    consumers: ConsumerState
    world_params: WorldParams

    @property
    def world_state(self) -> WorldState:
        return WorldState(self.hotels, self.consumers)


    def step(self) -> None:
        self.consumers = realize_consumption(self.hotels, self.world_params)
        self.hotels = hotel_decisions(self.world_state, self.world_params)

    def run(self, n_steps: int) -> Generator[WorldState, None, None]:
        yield self.world_state
        for _ in range(n_steps):
            self.step()
            yield self.world_state
