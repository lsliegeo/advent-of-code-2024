import heapq
import math
from collections import defaultdict

from util.grid_util import Coordinate, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def parse_input(input_data: str) -> tuple[ListGrid, Coordinate, Coordinate]:
    start_index = input_data.index('S')
    goal_index = input_data.index('E')
    grid = ListGrid.from_input_string(input_data)
    start = Coordinate(start_index // (grid.max_y + 2), start_index % (grid.max_y + 2))
    goal = Coordinate(goal_index // (grid.max_y + 2), goal_index % (grid.max_y + 2))
    return grid, start, goal


def explore(grid: ListGrid, start: Coordinate, goal: Coordinate) -> dict[Coordinate]:
    distances: dict[Coordinate, float] = defaultdict(lambda: math.inf, {start: 0})
    queue: list[tuple[int, Coordinate]] = [(0, start)]

    while queue:
        distance, position = heapq.heappop(queue)

        # are we at the end?
        if position == goal:
            return dict(distances)

        # try to step
        for next_position in position.neighbours(diagonal=False).values():
            if grid.is_in_bounds(next_position) and grid[next_position.x][next_position.y] != '#':
                new_distance = distance + 1
                if new_distance < distances[next_position]:
                    distances[next_position] = new_distance
                    heapq.heappush(queue, (new_distance, next_position))


def get_time_saves(grid: ListGrid, start: Coordinate, goal: Coordinate, cheat_length: int, time_save_threshold: int = 100) -> dict[int, int]:
    distances = explore(grid, start, goal)

    cheats = defaultdict(set)
    for x, line in list(enumerate(grid)):
        for y, char in enumerate(line):
            if char != '#':
                distance = distances[Coordinate(x, y)]
                for x_offset in range(-cheat_length, cheat_length + 1):
                    for y_offset in range(-cheat_length + abs(x_offset), cheat_length - abs(x_offset) + 1):
                        if x_offset or y_offset:
                            cheat_x = x + x_offset
                            cheat_y = y + y_offset
                            if grid.is_in_bounds(Coordinate(cheat_x, cheat_y)) and grid[cheat_x][cheat_y] != '#':
                                cheat_distance = distances[Coordinate(cheat_x, cheat_y)]
                                diff = cheat_distance - distance - abs(x_offset) - abs(y_offset)
                                if diff >= time_save_threshold:
                                    cheats[diff].add((x, y, cheat_x, cheat_y))

    cheats = {time_save: len(cheats) for time_save, cheats in cheats.items()}
    return cheats


def part1(input_data: str, time_save_threshold: int = 100) -> int:
    grid, start, goal = parse_input(input_data)
    cheats = get_time_saves(grid, start, goal, 2, time_save_threshold)
    return sum(number_cheats for time_save, number_cheats in cheats.items())


def part2(input_data: str, time_save_threshold: int = 100) -> int:
    grid, start, goal = parse_input(input_data)
    cheats = get_time_saves(grid, start, goal, 20, time_save_threshold)
    return sum(number_cheats for time_save, number_cheats in cheats.items())


if __name__ == '__main__':
    grid, start, goal = parse_input(EXAMPLE)
    assert explore(grid, start, goal)[goal] == 84

    assert get_time_saves(*parse_input(EXAMPLE), cheat_length=2, time_save_threshold=1) == {2: 14, 4: 14, 6: 2, 8: 4, 10: 2, 12: 3, 20: 1, 36: 1, 38: 1, 40: 1, 64: 1}  # fmt: skip
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert get_time_saves(*parse_input(EXAMPLE), cheat_length=20, time_save_threshold=50) == {50: 32, 52: 31, 54: 29, 56: 39, 58: 25, 60: 23, 62: 20, 64: 19, 66: 12, 68: 14, 70: 12, 72: 22, 74: 4, 76: 3}  # fmt: skip
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
