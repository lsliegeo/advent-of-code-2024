import heapq

from tqdm import tqdm

from util.grid_util import Coordinate, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def expore(grid: ListGrid, start: Coordinate, goal: Coordinate) -> int | None:
    distances = {}
    queue = [(0, start)]
    while queue:
        distance, co = heapq.heappop(queue)

        previous_known_distance = distances.get(co)
        if previous_known_distance is not None and distance >= previous_known_distance:
            continue

        distances[co] = distance

        if co == goal:
            return distance

        for next_co in co.neighbours(diagonal=False).values():
            if grid.is_in_bounds(next_co) and not grid[next_co.x][next_co.y]:
                heapq.heappush(queue, (distance + 1, next_co))

    return None


def part1(input_data: str, size: int = 70, bytes_to_fall: int = 1024) -> int:
    grid = ListGrid([[False for _ in range(size + 1)] for _ in range(size + 1)])
    for line in input_data.splitlines()[:bytes_to_fall]:
        x, y = map(int, line.split(','))
        grid[x][y] = True
    start = Coordinate(0, 0)
    goal = Coordinate(size, size)
    return expore(grid, start, goal)


def part2(input_data: str, size: int = 70) -> str:
    start = Coordinate(0, 0)
    goal = Coordinate(size, size)
    grid = ListGrid([[False for _ in range(size + 1)] for _ in range(size + 1)])
    for line in tqdm(input_data.splitlines()):
        x, y = map(int, line.split(','))
        grid[x][y] = True
        # Simply try to reach the exit after every iteration
        # Slow but it works ¯\_(ツ)_/¯
        if expore(grid, start, goal) is None:
            return f'{x},{y}'


if __name__ == '__main__':
    assert part1(EXAMPLE, size=6, bytes_to_fall=12) == 22
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE, size=6) == '6,1'
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
