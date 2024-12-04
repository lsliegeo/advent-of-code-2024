from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input

EXAMPLE = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

EXAMPLE2 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def get_word(grid: ListGrid, co: Coordinate, direction: Direction, length: int) -> str | None:
    """Get a word starting from a specific coordination."""
    word = ''
    current_co = co
    for _ in range(length):
        if not grid.is_in_bounds(current_co):
            return None
        word += grid[current_co.x][current_co.y]
        current_co = current_co.step(direction)
    return word


def get_words_part_1(grid: ListGrid, co: Coordinate) -> list[str]:
    """Get all words in all directions starting from a starting coordinate."""
    words = []
    for direction in Direction:
        if word := get_word(grid, co, direction, 4):
            words.append(word)
    return words


def part1(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    total = 0
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            if grid[x][y] == 'X':
                words = get_words_part_1(grid, Coordinate(x, y))
                total += words.count('XMAS')
    return total


def is_x_mas(grid: ListGrid, co: Coordinate) -> bool:
    """Returns whether there are 2 MAS centered around the coordinate."""
    word_one = get_word(grid, co.step(Direction.NORTH_WEST), Direction.SOUTH_EAST, 3)
    word_two = get_word(grid, co.step(Direction.NORTH_EAST), Direction.SOUTH_WEST, 3)
    return word_one in ('MAS', 'SAM') and word_two in ('MAS', 'SAM')


def part2(input_data: str) -> int:
    grid = ListGrid.from_input_string(input_data)
    total = 0
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            if grid[x][y] == 'A' and is_x_mas(grid, Coordinate(x, y)):
                total += 1
    return total


if __name__ == '__main__':
    assert part1(EXAMPLE) == 4
    assert part1(EXAMPLE2) == 18
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE2) == 9
    print(f'Solution for part 2 is: {part2(get_input())}')
