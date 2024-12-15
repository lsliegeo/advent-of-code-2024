import copy

from tqdm import tqdm

from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

EXAMPLE_2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

EXAMPLE_3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""


def modify_input(grid_str: str) -> str:
    return ''.join(
        {
            '\n': '\n',
            '#': '##',
            'O': '[]',
            '@': '@.',
            '.': '..',
        }[char]
        for char in grid_str
    )


def parse_input(input_data: str, part_2: bool = False) -> tuple[ListGrid, list[Direction], Coordinate]:
    grid_str, moves_str = input_data.split('\n\n')
    if part_2:
        grid_str = modify_input(grid_str)
    grid = ListGrid.from_input_string(grid_str)
    moves = [{'^': Direction.NORTH, 'v': Direction.SOUTH, '>': Direction.EAST, '<': Direction.WEST}[char] for char in moves_str if char != '\n']
    start_co = next(iter(Coordinate(x, y) for x in range(grid.max_x + 1) for y in range(grid.max_y + 1) if grid[x][y] == '@'))
    grid[start_co.x][start_co.y] = '.'
    return grid, moves, start_co


def execute_move_part_1(grid: ListGrid, current_position: Coordinate, direction: Direction) -> Coordinate:
    can_move = False
    for next_co in current_position.steps(direction):
        if not grid.is_in_bounds(next_co):
            break
        if grid[next_co.x][next_co.y] == '#':
            break
        if grid[next_co.x][next_co.y] == '.':
            can_move = True

    if can_move:
        current_position = current_position.step(direction)
        if grid[current_position.x][current_position.y] == 'O':
            # We need to push the boxes
            for next_co in current_position.steps(direction):
                if grid[next_co.x][next_co.y] == '.':
                    grid[next_co.x][next_co.y] = 'O'
                    break
        grid[current_position.x][current_position.y] = '.'

    return current_position


def part1(input_data: str) -> int:
    grid, moves, start_co = parse_input(input_data)

    current_position = start_co
    for direction in moves:
        current_position = execute_move_part_1(grid, current_position, direction)

    coordinates = []
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            if char == 'O':
                coordinates.append(x * 100 + y)

    return sum(coordinates)


def execute_move_part_2(i, _grid: ListGrid, current_position: Coordinate, direction: Direction) -> tuple[ListGrid, Coordinate]:
    # i'm tired boss
    grid = copy.deepcopy(_grid)
    next_position = current_position.step(direction)
    can_move = False
    if direction == Direction.WEST:
        first_empty_y = None
        for y in range(1, current_position.y):
            char = grid[current_position.x][y]
            if char == '.':
                first_empty_y = y
            elif char == '#':
                first_empty_y = None
        if first_empty_y is not None:
            to_shift = grid[current_position.x][first_empty_y : current_position.y]
            shifted = to_shift[1:] + ['.']
            grid[current_position.x][first_empty_y : current_position.y] = shifted
            can_move = True

    elif direction == Direction.EAST:
        first_empty_y = None
        for y in reversed(range(current_position.y + 1, grid.max_y)):
            char = grid[current_position.x][y]
            if char == '.':
                first_empty_y = y
            elif char == '#':
                first_empty_y = None
        if first_empty_y is not None:
            to_shift = grid[current_position.x][current_position.y + 1 : first_empty_y + 1]
            shifted = ['.'] + to_shift[:-1]
            grid[current_position.x][current_position.y + 1 : first_empty_y + 1] = shifted
            can_move = True

    elif direction in (Direction.NORTH, Direction.SOUTH):
        can_move = True
        blocking_position_to_replace_position = {next_position: False}
        current_x = current_position.x
        next_x = next_position.x
        while blocking_position_to_replace_position:
            previous_x = current_x
            current_x = next_x
            next_x = current_x + 1 if direction == Direction.SOUTH else current_x - 1
            additional_blocking_positions = {}
            for blocking_co, replace_position in blocking_position_to_replace_position.items():
                if _grid[blocking_co.x][blocking_co.y] == ']':
                    additional_blocking_positions[blocking_co.step(Direction.WEST)] = False
                elif _grid[blocking_co.x][blocking_co.y] == '[':
                    additional_blocking_positions[blocking_co.step(Direction.EAST)] = False
            blocking_position_to_replace_position = additional_blocking_positions | blocking_position_to_replace_position
            new_blocking_positions = {}
            for blocking_co, replace_position in blocking_position_to_replace_position.items():
                char = _grid[blocking_co.x][blocking_co.y]
                next_co = blocking_co.step(direction)
                if char == '#':
                    can_move = False
                    break
                elif char in '[]':
                    new_blocking_positions[next_co] = True
                elif char == '.':
                    continue
                # update the next tile
                grid[next_x][next_co.y] = _grid[current_x][blocking_co.y]
                # update the current tile
                if replace_position:
                    grid[current_x][blocking_co.y] = _grid[previous_x][blocking_co.y]
                else:
                    grid[current_x][blocking_co.y] = '.'
            blocking_position_to_replace_position = new_blocking_positions

    if can_move:
        return grid, next_position
    else:
        return _grid, current_position


def part2(input_data: str) -> int:
    grid, moves, start_co = parse_input(input_data, part_2=True)

    current_position = start_co
    for i, direction in tqdm(list(enumerate(moves))):
        # print(i)
        # print(direction)
        grid, current_position = execute_move_part_2(i, grid, current_position, direction)
        # grid[current_position.x][current_position.y] = '@'
        # grid.visualize()
        # grid[current_position.x][current_position.y] = '.'

    coordinates = []
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            if char == '[':
                best_y_distance = y
                coordinates.append(x * 100 + best_y_distance)

    return sum(coordinates)


if __name__ == '__main__':
    assert part1(EXAMPLE_2) == 2028
    assert part1(EXAMPLE) == 10092
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    part2(EXAMPLE_3)
    assert (
        part2("""#######
#.....#
#.....#
#.@O..#
#..#O.#
#...O.#
#..O..#
#.....#
#######

>><vvv>v>^^^""")
        == 1430
    )
    assert part2(EXAMPLE) == 9021
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
