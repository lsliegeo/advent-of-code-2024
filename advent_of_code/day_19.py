import functools
import re

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse_input(input_data: str) -> tuple[list[str], list[str]]:
    towels_str, designs_str = input_data.split('\n\n')
    towels = towels_str.split(', ')
    designs = designs_str.splitlines()
    return towels, designs


def part1(input_data: str) -> int:
    towels, designs = parse_input(input_data)
    regex = re.compile(rf'^({"|".join(towels)})*$')
    return sum(re.match(regex, towel) is not None for towel in designs)


def part2(input_data: str) -> int:
    towels, designs = parse_input(input_data)
    design_to_towels = {
        design: [
            towel
            for towel in towels
            if towel in design
        ]  # fmt: skip
        for design in designs
    }  # fmt: skip

    @functools.cache
    def get_number_combinations(design: str, position: int = 0) -> int:
        if position == len(design):
            return 1
        elif position > len(design):
            return 0
        number_combinations = 0
        for towel in design_to_towels[design]:
            if design[position : position + len(towel)] == towel:
                number_combinations += get_number_combinations(design, position + len(towel))
        return number_combinations

    return sum(get_number_combinations(design) for design in designs)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 6
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 16
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
