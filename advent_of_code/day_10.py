from collections import defaultdict

from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def get_routes(input_data: str, part_1: bool) -> int:
    topographic_map = ListGrid.from_input_string(input_data, cast=lambda x: None if x == '.' else int(x))

    # preprocess next steps
    height_to_coordinate_to_next_coordinates = defaultdict(lambda: defaultdict(list))
    for x in range(topographic_map.max_x + 1):
        for y in range(topographic_map.max_y + 1):
            co = Coordinate(x, y)
            height = topographic_map[x][y]
            if height and height > 0:
                for direction in Direction.orthogonal_directions():
                    next_co = co.step(direction)
                    if topographic_map.is_in_bounds(next_co) and topographic_map[next_co.x][next_co.y] == height - 1:
                        height_to_coordinate_to_next_coordinates[height][co].append(next_co)

    # for storing the intermediate result
    distinct_trails = ListGrid([[0 for _ in range(topographic_map.max_y + 1)] for _ in range(topographic_map.max_x + 1)])
    trails = defaultdict(set)
    for co in height_to_coordinate_to_next_coordinates[9]:
        distinct_trails[co.x][co.y] = 1
        trails[co].add(co)

    # delegate the number of routes, fully processing a single height before proceeding to the next one
    for height in range(9, 0, -1):
        for co, next_cos in height_to_coordinate_to_next_coordinates[height].items():
            for next_co in next_cos:
                distinct_trails[next_co.x][next_co.y] += distinct_trails[co.x][co.y]
                trails[next_co].update(trails[co])

    if part_1:
        return sum(len(trails[Coordinate(x, y)]) for x in range(topographic_map.max_y + 1) for y in range(topographic_map.max_x + 1) if topographic_map[x][y] == 0)
    else:
        return sum(distinct_trails[x][y] for x in range(topographic_map.max_y + 1) for y in range(topographic_map.max_x + 1) if topographic_map[x][y] == 0)


def part1(input_data: str) -> int:
    return get_routes(input_data, True)


def part2(input_data: str) -> int:
    return get_routes(input_data, False)


if __name__ == '__main__':
    assert (
        part1("""...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9""")
        == 2
    )
    assert (
        part1("""..90..9
...1.98
...2..7
6543456
765.987
876....
987....""")
        == 4
    )
    assert (
        part1("""10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""")
        == 3
    )
    assert part1(EXAMPLE) == 36
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert (
        part2(""".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""")
        == 3
    )
    assert (
        part2("""..90..9
...1.98
...2..7
6543456
765.987
876....
987....""")
        == 13
    )
    assert (
        part2("""012345
123456
234567
345678
4.6789
56789.""")
        == 227
    )
    assert part2(EXAMPLE) == 81
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
