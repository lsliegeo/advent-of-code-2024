import functools
from math import floor, log10

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """125 17"""


@functools.cache
def blink(stone: int) -> list[int]:
    """Advance a single stone a single time, resulting in a list of either one or two stones."""
    if stone == 0:
        return [1]
    elif (number_digits := floor(log10(stone)) + 1) and number_digits % 2 == 0:
        right_half = stone % 10 ** (number_digits / 2)
        left_half = (stone - right_half) / 10 ** (number_digits / 2)
        return [int(left_half), int(right_half)]
    else:
        return [stone * 2024]


@functools.cache
def get_number_of_stones(stone: int, number_of_blinks: int) -> int:
    """Advance a single stone and its subsequent stones any number of times, returning the number of stones in the end."""
    next_stones = blink(stone)
    if number_of_blinks < 1:
        raise Exception('Unexpected number of blinks')
    elif number_of_blinks == 1:
        return len(next_stones)
    else:
        return sum(get_number_of_stones(next_stone, number_of_blinks - 1) for next_stone in next_stones)


def part1(input_data: str) -> int:
    stones = list(map(int, input_data.split()))
    return sum(get_number_of_stones(stone, 25) for stone in stones)


def part2(input_data: str) -> int:
    stones = list(map(int, input_data.split()))
    return sum(get_number_of_stones(stone, 75) for stone in stones)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 55312
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
