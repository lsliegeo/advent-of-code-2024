import functools
import itertools

from util.grid_util import Coordinate, Direction
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """029A
980A
179A
456A
379A"""

NUMERICAL_KEYMAP_LAYOUT = {
    Coordinate(0, 0): '7',
    Coordinate(0, 1): '8',
    Coordinate(0, 2): '9',
    Coordinate(1, 0): '4',
    Coordinate(1, 1): '5',
    Coordinate(1, 2): '6',
    Coordinate(2, 0): '1',
    Coordinate(2, 1): '2',
    Coordinate(2, 2): '3',
    Coordinate(3, 1): '0',
    Coordinate(3, 2): 'A',
}

DIRECTIONAL_KEYMAP_LAYOUT = {
    Coordinate(0, 1): '^',
    Coordinate(0, 2): 'A',
    Coordinate(1, 0): '<',
    Coordinate(1, 1): 'v',
    Coordinate(1, 2): '>',
}

DIRECTION_STRING_TO_DIRECTION = {
    '^': Direction.NORTH,
    'v': Direction.SOUTH,
    '<': Direction.WEST,
    '>': Direction.EAST,
}

DIRECTION_TO_DIRECTION_STRING = {v: k for k, v in DIRECTION_STRING_TO_DIRECTION.items()}


def get_routes(start: Coordinate, goal: Coordinate, allowed_positions: set[Coordinate]) -> list[list[Direction]]:
    distance = Coordinate.manhattan_distance(start, goal)
    x_direction = Direction.EAST if start.y < goal.y else Direction.WEST
    y_direction = Direction.SOUTH if start.x < goal.x else Direction.NORTH

    valid_routes = []
    for route in itertools.product([x_direction, y_direction], repeat=distance):
        valid = True
        current = start
        for direction in route:
            current = current.step(direction)
            if current not in allowed_positions:
                valid = False
                break
        if valid and current == goal:
            valid_routes.append(route)

    return valid_routes


def generate_keymap(layout: dict[Coordinate, str]) -> dict[tuple[str, str], list[str]]:
    keymap = {}
    for co_a, co_b in itertools.product(layout, layout):
        if co_a == co_b:
            keymap[(layout[co_a], layout[co_b])] = []
        else:
            routes = get_routes(co_a, co_b, set(layout))
            keymap[(layout[co_a], layout[co_b])] = [''.join([DIRECTION_TO_DIRECTION_STRING[d] for d in r]) for r in routes]
    return keymap


NUMERICAL_KEYMAP = generate_keymap(NUMERICAL_KEYMAP_LAYOUT)
DIRECTIONAL_KEYMAP = generate_keymap(DIRECTIONAL_KEYMAP_LAYOUT)


@functools.cache
def get_shortest_sequence(code: str, total_robots: int, robot_number: int = 0) -> int:
    lookup_keymap = NUMERICAL_KEYMAP if robot_number == 0 else DIRECTIONAL_KEYMAP

    if robot_number > total_robots:
        return len(code)

    previous = 'A'
    total_cost = 0
    for char in code:
        routes = lookup_keymap[(previous, char)]
        sequences_lengths = [get_shortest_sequence(route + 'A', total_robots, robot_number + 1) for route in routes]
        if sequences_lengths:
            total_cost += min(sequences_lengths)
        else:
            total_cost += 1
        previous = char

    return total_cost


def part1(input_data: str) -> int:
    total_complexity = 0
    for code in input_data.splitlines():
        numeric_part = int(code[:-1])
        shortest_sequence_length = get_shortest_sequence(code, 2)
        total_complexity += numeric_part * shortest_sequence_length
    return total_complexity


def part2(input_data: str) -> int:
    total_complexity = 0
    for code in input_data.splitlines():
        numeric_part = int(code[:-1])
        shortest_sequence_length = get_shortest_sequence(code, 25)
        total_complexity += numeric_part * shortest_sequence_length
    return total_complexity


if __name__ == '__main__':
    assert part1(EXAMPLE) == 126384
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')
        # 13 seconds

    with ContextTimer():
        solution = part2(get_input())
        assert solution < 524110008179112
        print(f'Solution for part 2 is: {solution}')
