from __future__ import annotations

import abc
import dataclasses
from collections import UserDict, UserList
from enum import Enum


class Direction(Enum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'
    NORTH_WEST = 'north_west'
    NORTH_EAST = 'north_east'
    SOUTH_EAST = 'south_east'
    SOUTH_WEST = 'south_west'

    @staticmethod
    def orthogonal_directions() -> list[Direction]:
        return [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ]

    @staticmethod
    def diagonal_directions() -> list[Direction]:
        return [
            Direction.NORTH_EAST,
            Direction.NORTH_WEST,
            Direction.SOUTH_EAST,
            Direction.SOUTH_WEST,
        ]

    @staticmethod
    def opposite(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
            Direction.NORTH_EAST: Direction.SOUTH_WEST,
            Direction.SOUTH_WEST: Direction.NORTH_EAST,
            Direction.NORTH_WEST: Direction.SOUTH_EAST,
            Direction.SOUTH_EAST: Direction.NORTH_WEST,
        }[direction]

    @staticmethod
    def rotate(direction: Direction, left: bool) -> Direction:
        mapping = {
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
            Direction.EAST: Direction.SOUTH,
            Direction.NORTH_EAST: Direction.SOUTH_EAST,
            Direction.SOUTH_WEST: Direction.NORTH_WEST,
            Direction.NORTH_WEST: Direction.NORTH_EAST,
            Direction.SOUTH_EAST: Direction.SOUTH_WEST,
        }
        if left:
            mapping = {v: k for k, v in mapping.items()}
        return mapping[direction]


@dataclasses.dataclass(frozen=True)
class Coordinate:
    """
    Origin is upper left corner.

    +------->
    |      (y)
    |
    |
    v (x)
    """

    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def step(self, direction: Direction, amount: int = 1):
        assert isinstance(direction, Direction)
        match direction:
            case Direction.NORTH | Direction.NORTH_EAST | Direction.NORTH_WEST:
                x_diff = -1
            case Direction.SOUTH | Direction.SOUTH_EAST | Direction.SOUTH_WEST:
                x_diff = 1
            case _:
                x_diff = 0
        match direction:
            case Direction.EAST | Direction.NORTH_EAST | Direction.SOUTH_EAST:
                y_diff = 1
            case Direction.WEST | Direction.NORTH_WEST | Direction.SOUTH_WEST:
                y_diff = -1
            case _:
                y_diff = 0
        return Coordinate(self.x + x_diff * amount, self.y + y_diff * amount)

    def neighbours(self, diagonal: bool) -> dict[Direction, Coordinate]:
        directions = list(Direction) if diagonal else Direction.orthogonal_directions()
        return {direction: self.step(direction) for direction in directions}

    @staticmethod
    def manhattan_distance(co_1: Coordinate, co_2: Coordinate) -> int:
        return abs(co_1.x - co_2.x) + abs(co_1.y - co_2.y)


class Grid(abc.ABC):
    @property
    @abc.abstractmethod
    def min_x(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def max_x(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def min_y(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def max_y(self) -> int:
        raise NotImplementedError()

    def is_in_bounds(self, co: Coordinate) -> bool:
        return self.min_x <= co.x <= self.max_x and self.min_y <= co.y <= self.max_y

    def to_string(self, filler: str = '.') -> list[str]:
        raise NotImplementedError()

    def visualize(self, filler: str = '.'):
        print('\n'.join(self.to_string(filler)))
        print()


class DictGrid(Grid, UserDict):
    """
    Origin is upper left corner.

    +------->
    |      (y)
    |
    |
    v (x)
    """

    def to_string(self, filler: str = '.') -> list[str]:
        lines = []
        for x in range(self.min_x, self.max_x + 1):
            lines.append('')
            for y in range(self.min_x, self.max_y + 1):
                value = self.data.get(Coordinate(x, y), filler)
                if isinstance(value, Enum):
                    value = value.value
                lines[-1] += value
        return lines

    @property
    def min_x(self) -> int:
        return min(co.x for co in self.data)

    @property
    def max_x(self) -> int:
        return max(co.x for co in self.data)

    @property
    def max_y(self) -> int:
        return max(co.y for co in self.data)

    @property
    def min_y(self) -> int:
        return min(co.y for co in self.data)


class ListGrid(Grid, UserList):
    """
    Origin is upper left corner.

    +------->
    |      (y)
    |
    |
    v (x)
    """

    def to_string(self, filler: str = '.') -> list[str]:
        return [''.join(value.value if isinstance(value, Enum) else value for value in line) for line in self.data]

    @property
    def min_x(self) -> int:
        return 0

    @property
    def max_x(self) -> int:
        return len(self.data) - 1

    @property
    def min_y(self) -> int:
        return 0

    @property
    def max_y(self) -> int:
        return len(self.data[0]) - 1

    @classmethod
    def from_input_string(cls, input_data: str) -> ListGrid:
        return cls([list(line) for line in input_data.splitlines()])
