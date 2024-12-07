import math

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def _forward(target: int, numbers: tuple[int], allow_concat: bool = False) -> bool:
    intermediate_results = [numbers[0]]
    for number in numbers[1:]:
        new_intermediate_results = [
            intermediate_result + number
            for intermediate_result in intermediate_results
            if intermediate_result + number <= target
        ] + [
            intermediate_result * number
            for intermediate_result in intermediate_results
            if intermediate_result * number <= target
        ]  # fmt: skip
        if allow_concat:
            new_intermediate_results += [
                intermediate_result * 10 ** len(str(number)) + number
                for intermediate_result in intermediate_results
                if intermediate_result * 10 ** len(str(number)) + number <= target
            ]  # fmt: skip
        intermediate_results = new_intermediate_results
    return target in intermediate_results


def _backward(current: int, numbers: tuple[int], i: int, allow_concat: bool = False) -> bool:
    if i == 0:
        return current == numbers[0]

    after_undo_add = current - numbers[i]
    can_undo_add = after_undo_add >= 0 and _backward(after_undo_add, numbers, i - 1, allow_concat)

    after_undo_mul = current / numbers[i]
    can_undo_mul = math.floor(after_undo_mul) == math.ceil(after_undo_mul) and _backward(int(after_undo_mul), numbers, i - 1, allow_concat)

    can_undo_concat = False
    if allow_concat:
        after_undo_concat = (current - numbers[i]) / 10 ** len(str(numbers[i]))
        can_undo_concat = math.floor(after_undo_concat) == math.ceil(after_undo_concat) and _backward(int(after_undo_concat), numbers, i - 1, allow_concat)

    return can_undo_add or can_undo_mul or can_undo_concat


def part1(input_data: str, forward: bool = False) -> int:
    total = 0
    for line in input_data.splitlines():
        target, numbers = line.split(': ')
        target = int(target)
        numbers = tuple(map(int, numbers.split()))
        if forward and _forward(target, numbers):
            total += target
        elif not forward and _backward(target, numbers, len(numbers) - 1):
            total += target
    return total


def part2(input_data: str, forward: bool = False) -> int:
    total = 0
    for line in input_data.splitlines():
        target, numbers = line.split(': ')
        target = int(target)
        numbers = tuple(map(int, numbers.split()))
        if forward and _forward(target, numbers, allow_concat=True):
            total += target
        elif not forward and _backward(target, numbers, len(numbers) - 1, allow_concat=True):
            total += target
    return total


if __name__ == '__main__':
    assert part1(EXAMPLE, forward=True) == 3749
    with ContextTimer(threshold=0):
        print(f'Solution for part 1 (forward) is: {part1(get_input(), forward=True)}')
    assert part2(EXAMPLE, forward=True) == 11387
    with ContextTimer(threshold=0):
        print(f'Solution for part 2 (forward) is: {part2(get_input(), forward=True)}')

    assert part1(EXAMPLE, forward=False) == 3749
    with ContextTimer(threshold=0):
        print(f'Solution for part 1 (backward) is: {part1(get_input(), forward=False)}')
    assert part2(EXAMPLE, forward=False) == 11387
    with ContextTimer(threshold=0):
        print(f'Solution for part 2 (backward) is: {part2(get_input(), forward=False)}')
