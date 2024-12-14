import dataclasses
import math
import re
import shutil
from collections import defaultdict
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from util.grid_util import Coordinate
from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


@dataclasses.dataclass
class Robot:
    start_co: Coordinate
    velocity: Coordinate


def parse_input(input_data: str) -> list[Robot]:
    robots = []
    for line in input_data.splitlines():
        ints = list(map(int, re.match(r'p=([-0-9]*),([-0-9]*) v=([-0-9]*),([-0-9]*)', line).groups()))
        robots.append(
            Robot(
                start_co=Coordinate(ints[0], ints[1]),
                velocity=Coordinate(ints[2], ints[3]),
            )
        )
    return robots


def simulate_robot(robot: Robot, width: int, height: int, seconds: int) -> Coordinate:
    return Coordinate(
        x=(robot.start_co.x + seconds * robot.velocity.x) % width,
        y=(robot.start_co.y + seconds * robot.velocity.y) % height,
    )


def get_quadrant(co: Coordinate, width: int, height: int) -> tuple[bool, bool] | None:
    middle_x = (width - 1) // 2
    middle_y = (height - 1) // 2
    if co.x == middle_x or co.y == middle_y:
        return None
    return co.x < middle_x, co.y < middle_y


def part1(input_data: str, width: int = 101, height: int = 103) -> int:
    robots = parse_input(input_data)
    final_coordinates = [simulate_robot(robot, width, height, 100) for robot in robots]
    quadrant_to_coordinates = defaultdict(list)
    for co in final_coordinates:
        quadrant = get_quadrant(co, width, height)
        quadrant_to_coordinates[quadrant].append(co)
    safety_factor = 1
    for quadrant, coordinates in quadrant_to_coordinates.items():
        if quadrant is not None:
            safety_factor *= len(coordinates)
    return safety_factor


def part2(input_data: str, width: int = 101, height: int = 103):
    robots = parse_input(input_data)

    image_directory = Path(__file__).parent.parent / 'day_14_images'
    try:
        shutil.rmtree(image_directory)
    except Exception:
        pass
    image_directory.mkdir()

    iterations = 10000
    filename_padding_length = math.floor(math.log10(iterations - 1)) + 1
    for seconds in tqdm(range(iterations)):
        coordinates = [simulate_robot(robot, width, height, seconds) for robot in robots]
        create_image(coordinates, width, height, (image_directory / f'{seconds:0{filename_padding_length}d}.bmp').as_posix())


def create_image(white_pixel_coordinates: list[Coordinate], width: int, height: int, filename: str):
    img = Image.new('RGB', (width, height), 'black')
    for co in white_pixel_coordinates:
        img.putpixel((co.x, co.y), (255, 255, 255))
    img.save(filename)


if __name__ == '__main__':
    assert simulate_robot(Robot(Coordinate(2, 4), Coordinate(2, -3)), 11, 7, 1) == Coordinate(4, 1)
    assert simulate_robot(Robot(Coordinate(2, 4), Coordinate(2, -3)), 11, 7, 2) == Coordinate(6, 5)
    assert simulate_robot(Robot(Coordinate(2, 4), Coordinate(2, -3)), 11, 7, 5) == Coordinate(1, 3)
    assert part1(EXAMPLE, 11, 7) == 12
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    with ContextTimer():
        part2(get_input())
        print('Solution for part 2 is: have fun scrolling through the images')
        # 7916
