from collections import defaultdict
from itertools import combinations

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

EXAMPLE_2 = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""


def part1(input_data: str) -> int:
    max_x = len(input_data.splitlines())
    max_y = len(input_data.splitlines()[0])

    antenna_to_positions: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for x, line in enumerate(input_data.splitlines()):
        for y, char in enumerate(line):
            if char != '.':
                antenna_to_positions[char].append((x, y))

    antinodes: set[tuple[int, int]] = set()
    for antenna_char, positions in antenna_to_positions.items():
        for pos_1, pos_2 in combinations(positions, 2):
            pos_1_to_2_x = pos_2[0] - pos_1[0]
            pos_1_to_2_y = pos_2[1] - pos_1[1]
            antinodes.add((pos_2[0] + pos_1_to_2_x, pos_2[1] + pos_1_to_2_y))
            antinodes.add((pos_1[0] - pos_1_to_2_x, pos_1[1] - pos_1_to_2_y))

    return len({
        antinode
        for antinode in antinodes
        if (
            0 <= antinode[0] < max_x
            and 0 <= antinode[1] < max_y
        )
    })  # fmt: skip


def part2(input_data: str) -> int:
    max_x = len(input_data.splitlines())
    max_y = len(input_data.splitlines()[0])

    antenna_to_positions: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for x, line in enumerate(input_data.splitlines()):
        for y, char in enumerate(line):
            if char != '.':
                antenna_to_positions[char].append((x, y))

    antinodes: set[tuple[int, int]] = set()
    for antenna_char, positions in antenna_to_positions.items():
        for pos_1, pos_2 in combinations(positions, 2):
            pos_1_to_2_x = pos_2[0] - pos_1[0]
            pos_1_to_2_y = pos_2[1] - pos_1[1]

            behind_pos_2 = pos_2
            while 0 <= behind_pos_2[0] < max_x and 0 <= behind_pos_2[1] < max_y:
                antinodes.add(behind_pos_2)
                behind_pos_2 = (behind_pos_2[0] + pos_1_to_2_x, behind_pos_2[1] + pos_1_to_2_y)

            before_pos_1 = pos_1
            while 0 <= before_pos_1[0] < max_x and 0 <= before_pos_1[1] < max_y:
                antinodes.add(before_pos_1)
                before_pos_1 = (before_pos_1[0] - pos_1_to_2_x, before_pos_1[1] - pos_1_to_2_y)

    return len(antinodes)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 14
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE_2) == 9
    assert part2(EXAMPLE) == 34
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
