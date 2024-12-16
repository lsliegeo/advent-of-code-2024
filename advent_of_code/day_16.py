import heapq
import math
from collections import defaultdict

from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

EXAMPLE_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


def heuristic(position: Coordinate, direction: Direction, goal: Coordinate) -> int:
    x_is_correct = position.x == goal.x
    y_is_correct = position.y == goal.y
    x_facing_the_right_way = position.x < goal.x == (direction == Direction.SOUTH)
    y_facing_the_right_way = position.y < goal.y == (direction == Direction.EAST)

    turns_needed = 0
    if not x_is_correct and not x_facing_the_right_way:
        turns_needed += 1
    if not y_is_correct and not y_facing_the_right_way:
        turns_needed += 1

    return 1000 * turns_needed + Coordinate.manhattan_distance(position, goal)


def explore(grid: ListGrid, start_direction: Direction, start: Coordinate, goal: Coordinate) -> dict[Coordinate, dict[Direction, float]]:
    best_score = math.inf
    scores: dict[Coordinate, dict[Direction, float]] = defaultdict(lambda: defaultdict(lambda: math.inf))
    queue: list[tuple[int, Coordinate, Direction]] = [(0, start, start_direction)]

    while queue:
        current_score, position, direction = heapq.heappop(queue)

        # stop if we already got here in a better way
        if scores[position][direction] < current_score:
            continue

        # stop if it's already worse than the best score
        best_possible_score = current_score + heuristic(position, direction, goal)
        if best_possible_score > best_score:
            continue

        # are we at the end?
        if position == goal:
            best_score = min(best_score, current_score)
            continue

        # try to step
        next_position = position.step(direction)
        if grid[next_position.x][next_position.y] != '#':
            new_score = current_score + 1
            if new_score < scores[next_position][direction]:
                scores[next_position][direction] = new_score
                heapq.heappush(queue, (new_score, next_position, direction))

        # try to rotate
        for left in (True, False):
            next_direction = Direction.rotate(direction, left=left)
            new_score = current_score + 1000
            if new_score < scores[position][next_direction]:
                scores[position][next_direction] = new_score
                heapq.heappush(queue, (new_score, position, next_direction))

    return scores


def part1(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    start = Coordinate(grid.max_x - 1, 1)
    goal = Coordinate(1, grid.max_y - 1)
    scores = explore(grid, Direction.EAST, start, goal)
    return int(min(scores[goal].values()))


def part2(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    start = Coordinate(grid.max_x - 1, 1)
    goal = Coordinate(1, grid.max_y - 1)
    scores = explore(grid, Direction.EAST, start, goal)

    best_score = int(min(scores[goal].values()))
    tiles = set()
    to_explore = {(goal, direction, score) for direction, score in scores[goal].items() if score == best_score}
    while to_explore:
        position, direction, score = to_explore.pop()
        tiles.add(position)

        # try to step back
        previous_position = position.step(Direction.opposite(direction))
        previous_score = score - 1
        if scores[previous_position][direction] == previous_score:
            to_explore.add((previous_position, direction, previous_score))

        # try to rotate
        for left in (True, False):
            previous_direction = Direction.rotate(direction, left=left)
            previous_score = score - 1000
            if scores[position][previous_direction] == previous_score:
                to_explore.add((position, previous_direction, previous_score))

    return len(tiles)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 7036
    assert part1(EXAMPLE_2) == 11048
    assert part1(get_input()) == 82460
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 45
    assert part2(EXAMPLE_2) == 64
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
