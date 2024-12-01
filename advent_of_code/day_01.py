from collections import defaultdict

from util.input_util import get_input

EXAMPLE = """3   4
4   3
2   5
1   3
3   9
3   3"""


def part1(input_data: str) -> int:
    left = [int(l.split()[0]) for l in input_data.splitlines()]
    right = [int(l.split()[1]) for l in input_data.splitlines()]
    return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right), strict=True))


def part2(input_data: str) -> int:
    left = [int(l.split()[0]) for l in input_data.splitlines()]
    right = [int(l.split()[1]) for l in input_data.splitlines()]

    right_to_count = defaultdict(int)
    for i in right:
        right_to_count[i] += 1

    return sum(i * right_to_count[i] for i in left)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 11
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 31
    print(f'Solution for part 2 is: {part2(get_input())}')
