from collections import defaultdict
from collections.abc import Iterator

from util.grid_util import Coordinate, Direction, ListGrid
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """AAAA
BBCD
BBCC
EEEC"""

EXAMPLE_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

EXAMPLE_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

EXAMPLE_4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

EXAMPLE_5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


def get_areas(input_data: str) -> Iterator[tuple[str, set[Coordinate]]]:
    grid = ListGrid.from_input_string(input_data)

    # preprocessing
    plant_type_to_coordinate_to_neighbours: dict[str, dict[Coordinate, list[Coordinate]]] = defaultdict(dict)
    for x in range(grid.max_x + 1):
        for y in range(grid.max_y + 1):
            plant_type = grid[x][y]
            coordinate = Coordinate(x, y)
            plant_type_to_coordinate_to_neighbours[plant_type][coordinate] = []
            for neighbour in coordinate.neighbours(diagonal=False).values():
                if grid.is_in_bounds(neighbour) and grid[neighbour.x][neighbour.y] == plant_type:
                    plant_type_to_coordinate_to_neighbours[plant_type][coordinate].append(neighbour)

    for plant_type, coordinate_to_neighbours in plant_type_to_coordinate_to_neighbours.items():
        # tile_id = the index of a coordinate. This doesn't change.
        # plot_id = id of the plot. When 2 plots get merged, the lowest plot id will remain.

        coordinate_to_tile_id = {co: i for i, co in enumerate(coordinate_to_neighbours)}
        plot_id_to_coordinates = {i: {co} for i, co in enumerate(coordinate_to_neighbours)}
        tile_id_to_plot_id = {i: i for i in range(len(coordinate_to_tile_id))}

        to_explore = set(coordinate_to_neighbours)
        while to_explore:
            coordinate = to_explore.pop()

            for neighbour in coordinate_to_neighbours[coordinate]:
                # these neighbours are 1 tile away and from the same plant type

                coordinate_tile_id = coordinate_to_tile_id[coordinate]
                coordinate_plot_id = tile_id_to_plot_id[coordinate_tile_id]
                neighbour_tile_id = coordinate_to_tile_id[neighbour]
                neighbour_plot_id = tile_id_to_plot_id[neighbour_tile_id]

                # 1. merge the coordinates of both plots
                # 2. make the weaker tile point to the new plot
                # 3. explore starting from the weaker tile
                if coordinate_plot_id < neighbour_plot_id:
                    plot_id_to_coordinates[coordinate_plot_id].update(plot_id_to_coordinates[neighbour_plot_id])
                    tile_id_to_plot_id[neighbour_tile_id] = coordinate_plot_id
                    to_explore.add(neighbour)
                elif coordinate_plot_id > neighbour_plot_id:
                    plot_id_to_coordinates[neighbour_plot_id].update(plot_id_to_coordinates[coordinate_plot_id])
                    tile_id_to_plot_id[coordinate_tile_id] = neighbour_plot_id
                    to_explore.add(coordinate)

        for plot_id in set(tile_id_to_plot_id.values()):
            yield plant_type, plot_id_to_coordinates[plot_id]


def part1(input_data: str) -> int:
    price = 0
    for _, coordinates in get_areas(input_data):
        area = len(coordinates)
        perimeter = area * 4
        for coordinate in coordinates:
            for neighbour in coordinate.neighbours(diagonal=False).values():
                if neighbour in coordinates:
                    perimeter -= 1
        price += area * perimeter

    return price


def part2(input_data: str) -> int:
    price = 0
    for plant_type, coordinates in get_areas(input_data):
        area = len(coordinates)
        sides = 0

        # preprocessing
        # we need a fence for every direction which doesn't have a neighbour
        direction_to_fences: dict[Direction, set[Coordinate]] = defaultdict(set)
        for coordinate in coordinates:
            for direction, neighbour in coordinate.neighbours(diagonal=False).items():
                if neighbour not in coordinates:
                    direction_to_fences[direction].add(coordinate)

        # for every direction, every row/column, we'll scan for the number of breaks
        for fence_direction, fences in direction_to_fences.items():
            walk_direction = Direction.rotate(fence_direction, left=False)

            # group per row/column
            row_to_fences = defaultdict(list)
            for fence in fences:
                key = fence.y if walk_direction in (Direction.NORTH, Direction.SOUTH) else fence.x
                row_to_fences[key].append(fence)

            for row, row_fences in row_to_fences.items():
                row_fences = sorted(row_fences, reverse=walk_direction in (Direction.NORTH, Direction.WEST))
                sides += 1
                # iterate over the row/column
                for i in range(1, len(row_fences)):
                    if row_fences[i - 1].step(walk_direction) != row_fences[i]:
                        # a break in the row/column --> a new side starts here
                        sides += 1

        price += area * sides
    return price


if __name__ == '__main__':
    assert part1(EXAMPLE) == 140
    assert part1(EXAMPLE_2) == 772
    assert part1(EXAMPLE_3) == 1930
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 80
    assert part2(EXAMPLE_2) == 436
    assert part2(EXAMPLE_3) == 1206
    assert part2(EXAMPLE_4) == 236
    assert part2(EXAMPLE_5) == 368
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
