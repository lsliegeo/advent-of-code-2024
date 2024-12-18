import dataclasses

from tqdm import tqdm

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

EXAMPLE_2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


@dataclasses.dataclass
class Computer:
    a: int
    b: int
    c: int
    instructions: list[int]
    instruction_pointer: int = 0
    output: list[int] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.initial_a = self.a
        self.initial_b = self.b
        self.initial_c = self.c

    def execute_cycle(self):
        opcode = self.instructions[self.instruction_pointer]
        operand = self.instructions[self.instruction_pointer + 1]
        match opcode:
            case 0:  # adv
                self.a = self.a // (2 ** self.combo_operand(operand))
            case 1:  # bxl
                self.b = self.b ^ operand
            case 2:  # bst
                self.b = self.combo_operand(operand) % 8
            case 3:  # jnz
                if self.a:
                    self.instruction_pointer = operand
                    return
            case 4:  # bxc
                self.b = self.b ^ self.c
            case 5:  # out
                self.output.append(self.combo_operand(operand) % 8)
            case 6:  # bdv
                self.b = self.a // (2 ** self.combo_operand(operand))
            case 7:  # cdv
                self.c = self.a // (2 ** self.combo_operand(operand))
        self.instruction_pointer += 2

    def run_program(self):
        while self.instruction_pointer < len(self.instructions):
            self.execute_cycle()

    def reset(self):
        self.a = self.initial_a
        self.b = self.initial_b
        self.c = self.initial_c
        self.instruction_pointer = 0
        self.output = []

    def combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            raise Exception('Invalid combo operand')


def parse_input(input_data: str) -> Computer:
    registers_str, program_str = input_data.split('\n\n')
    registers_lines = registers_str.splitlines()
    instructions = list(map(int, program_str.split(' ')[-1].split(',')))
    computer = Computer(
        a=int(registers_lines[0].split(' ')[-1]),
        b=int(registers_lines[1].split(' ')[-1]),
        c=int(registers_lines[2].split(' ')[-1]),
        instructions=instructions,
    )
    return computer


def part1(input_data: str) -> str:
    computer = parse_input(input_data)
    computer.run_program()
    return ','.join(map(str, computer.output))


def part2(input_data: str) -> int:
    computer = parse_input(input_data)
    expected_output = computer.instructions
    candidates = {0}
    for i in tqdm(range(len(expected_output))):
        candidates = {(a << 3) + offset for a in candidates for offset in range(2**10)}
        # print(i, len(candidates))
        successful_candidates = set()
        for a in candidates:
            output = simulate_simplified(a)
            if output[: i + 1] == expected_output[-i - 1 :]:
                successful_candidates.add(a)
        candidates = successful_candidates

    a = min(candidates)
    assert simulate_simplified(a) == expected_output
    return a


def simulate_simplified(start: int) -> list[int]:
    a = start
    output = []
    while a:
        b = (a % 8) ^ 3
        c = a // (2**b)
        a = a // 8
        output.append((b ^ 5 ^ c) % 8)
    return output


if __name__ == '__main__':
    assert part1(EXAMPLE) == '4,6,3,5,6,3,5,2,1,0'
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
