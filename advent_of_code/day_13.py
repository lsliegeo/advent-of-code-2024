import dataclasses
import re

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


@dataclasses.dataclass
class SlotMachine:
    a: tuple[int, int]
    b: tuple[int, int]
    prize: tuple[int, int]


def parse_slot_machines(input_data: str, offset: int = 0) -> list[SlotMachine]:
    slot_machines = []
    for slot_machine_str in input_data.split('\n\n'):
        lines = slot_machine_str.splitlines()
        slot_machine = SlotMachine(
            a=tuple(map(int, re.search(r'X\+([0-9]+), Y\+([0-9]+)', lines[0]).groups())),
            b=tuple(map(int, re.search(r'X\+([0-9]+), Y\+([0-9]+)', lines[1]).groups())),
            prize=tuple(map(int, re.search(r'X=([0-9]+), Y=([0-9]+)', lines[2]).groups())),
        )
        if offset:
            slot_machine.prize = (slot_machine.prize[0] + offset, slot_machine.prize[1] + offset)
        slot_machines.append(slot_machine)
    return slot_machines


def get_combination_naive(slot_machine: SlotMachine) -> tuple[int, int] | None:
    base_x = base_y = 0
    for a_presses in range(101):
        if base_x > slot_machine.prize[0] or base_y > slot_machine.prize[1]:
            break
        current_x = base_x
        current_y = base_y
        for b_presses in range(101):
            if current_x == slot_machine.prize[0] and current_y == slot_machine.prize[1]:
                return a_presses, b_presses
            if current_x > slot_machine.prize[0] or current_y > slot_machine.prize[1]:
                break

            current_x += slot_machine.b[0]
            current_y += slot_machine.b[1]

        base_x += slot_machine.a[0]
        base_y += slot_machine.a[1]

    return None


def get_combination_cramer(slot_machine: SlotMachine) -> tuple[int, int] | None:
    """
    Cramer:
    a1 * x + b1 * y = c1
    a2 * x + b2 * y = c2
    ==>
    x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)

    in our case:
    a = button A
    b = button B
    c = prize
    x = number A presses
    y = number B presses
    """
    a1 = slot_machine.a[0]
    b1 = slot_machine.b[0]
    c1 = slot_machine.prize[0]
    a2 = slot_machine.a[1]
    b2 = slot_machine.b[1]
    c2 = slot_machine.prize[1]
    x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
    if x == int(x) and y == int(y):
        return int(x), int(y)
    return None


def part1(input_data: str) -> int:
    slot_machines = parse_slot_machines(input_data)
    total_tokens = 0
    for slot_machine in slot_machines:
        # if combination := get_combination_naive(slot_machine):
        #     a_presses, b_presses = combination
        #     total_tokens += 3 * a_presses + b_presses
        if combination := get_combination_cramer(slot_machine):
            a_presses, b_presses = combination
            if 0 <= a_presses <= 100 and 0 <= b_presses <= 100:
                total_tokens += 3 * a_presses + b_presses
    return total_tokens


def part2(input_data: str) -> int:
    slot_machines = parse_slot_machines(input_data, offset=10000000000000)
    total_tokens = 0
    for slot_machine in slot_machines:
        if combination := get_combination_cramer(slot_machine):
            a_presses, b_presses = combination
            total_tokens += 3 * a_presses + b_presses
    return total_tokens


if __name__ == '__main__':
    assert part1(EXAMPLE) == 480
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
        # 163365908498595 too high
