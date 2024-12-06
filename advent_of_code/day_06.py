import copy
from collections import defaultdict

from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def get_start_co(grid: ListGrid) -> Coordinate:
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            if grid[x][y] == '^':
                return Coordinate(x, y)
    raise ValueError('No start coordinate found')


def part1(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    start_co = get_start_co(grid)
    return simulate(grid, start_co, Direction.NORTH)


def part2(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    start_co = get_start_co(grid)
    current_co = start_co
    direction = Direction.NORTH
    positions_visited = defaultdict(set)
    loop_starts = set()
    while grid.is_in_bounds(current_co):
        positions_visited[current_co].add(direction)

        next_co = current_co.step(direction)
        if not grid.is_in_bounds(next_co):
            break

        if grid[next_co.x][next_co.y] == '#':
            direction = Direction.rotate(direction, left=False)
            continue
        elif next_co not in positions_visited:
            # if we would put an obstacle on the next position
            grid[next_co.x][next_co.y] = '#'
            try:
                simulate(grid, current_co, direction, copy.deepcopy(positions_visited)) is None
            except InfiniteLoopException:
                loop_starts.add(next_co)
                # print(len(positions_visited), len(loop_starts))
            grid[next_co.x][next_co.y] = '.'

        # grid[next_co.x][next_co.y] = 'X'
        current_co = next_co

    return len(loop_starts - {start_co})


class InfiniteLoopException(Exception):
    pass


def simulate(grid: ListGrid, current_co: Coordinate, direction: Direction, positions_visited: dict[Coordinate, set[Direction]] | None = None) -> int:
    if positions_visited is None:
        positions_visited = defaultdict(set)
    while grid.is_in_bounds(current_co):
        positions_visited[current_co].add(direction)

        next_co = current_co.step(direction)
        if not grid.is_in_bounds(next_co):
            break

        if grid[next_co.x][next_co.y] == '#':
            direction = Direction.rotate(direction, left=False)
            continue

        if direction in positions_visited[next_co]:
            raise InfiniteLoopException()

        # grid[next_co.x][next_co.y] = 'X'
        current_co = next_co

    return len(positions_visited)


if __name__ == '__main__':
    try:
        part1(""".#.
..#
...
.^.
...
#..
.#.""")
    except InfiniteLoopException:
        assert True
    else:
        assert False
    assert part1(EXAMPLE) == 41
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert (
        part2(""".#.#...
......#
.......
...^...
#......
.......
.......
.....#.""")
        == 3
    )
    assert (
        part2(""".#.
...
...
.^.
...
#..
.#.""")
        == 1
    )
    assert part2(EXAMPLE) == 6
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
        # 2102
        # 2101
        # 2134
