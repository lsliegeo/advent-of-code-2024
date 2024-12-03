import re

from util.input_util import get_input

EXAMPLE = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
EXAMPLE2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""


def solve(input_data: str, trim: bool) -> int:
    input_data = input_data.replace('\n', '')
    if trim:
        input_data = re.sub(r"don't\(\).*?(do\(\)|$)", '', input_data)
    total = 0
    for numbers in re.findall(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', input_data):
        total += int(numbers[0]) * int(numbers[1])
    return total


def part1(input_data: str) -> int:
    return solve(input_data, False)


def part2(input_data: str) -> int:
    return solve(input_data, True)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 161
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE2) == 48
    assert part2("mul(don't())mul(1,1)") == 0
    assert part2("don't(mul(1,1))") == 1
    print(f'Solution for part 2 is: {part2(get_input())}')
