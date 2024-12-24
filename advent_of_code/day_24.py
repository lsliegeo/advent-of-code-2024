import copy
import operator
from collections import defaultdict
from collections.abc import Callable

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

EXAMPLE_2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


def parse_input(input_data: str) -> tuple[dict[str, bool], dict[str, tuple[str, str, Callable[[bool, bool], bool]]]]:
    initial_values_str, gates_str = input_data.split('\n\n')

    initial_values = {}
    for line in initial_values_str.splitlines():
        name, value = line.split(': ')
        initial_values[name] = value == '1'

    gates = {}
    for line in gates_str.splitlines():
        input_str, output = line.split(' -> ')
        input_1, operation, input_2 = input_str.split(' ')
        operation = {
            'XOR': operator.xor,
            'OR': operator.or_,
            'AND': operator.and_,
        }[operation]
        gates[output] = (input_1, input_2, operation)

    return initial_values, gates


def simulate(initial_values: dict[str, bool], gates: dict[str, tuple[str, str, Callable[[bool, bool], bool]]]) -> dict[str, bool]:
    values = copy.deepcopy(initial_values)
    wire_to_where_it_can_be_used = defaultdict(list)
    for output, (input_1, input_2, operation) in gates.items():
        wire_to_where_it_can_be_used[input_1].append((output, input_2, operation))
        wire_to_where_it_can_be_used[input_2].append((output, input_1, operation))

    to_explore = set(values)
    while to_explore:
        wire = to_explore.pop()

        for output, other_input, operation in wire_to_where_it_can_be_used[wire]:
            if other_input in values:
                values[output] = operation(values[wire], values[other_input])
                to_explore.add(output)

    return values


def get_ints(values: dict[str, bool]) -> tuple[int, int, int]:
    x = sum(value * 2 ** int(wire[1:]) for wire, value in values.items() if wire[0] == 'x')
    y = sum(value * 2 ** int(wire[1:]) for wire, value in values.items() if wire[0] == 'y')
    z = sum(value * 2 ** int(wire[1:]) for wire, value in values.items() if wire[0] == 'z')
    return x, y, z


def part1(input_data: str) -> int:
    initial_values, gates = parse_input(input_data)
    values = simulate(initial_values, gates)
    return get_ints(values)[2]


def part2(input_data: str) -> str:
    initial_values_str, gates_str = input_data.split('\n\n')

    # these were manually found after visually checking the full adders drawn using mermaid js
    swaps = [
        ('z06', 'dhg'),
        ('dpd', 'brk'),
        ('bhd', 'z23'),
        ('nbf', 'z38'),
    ]
    for a, b in swaps:
        gates_str = gates_str.replace(f'-> {a}', '-> appelflap')
        gates_str = gates_str.replace(f'-> {b}', f'-> {a}')
        gates_str = gates_str.replace('-> appelflap', f'-> {b}')

    flowchart = [
        'flowchart LR',
        'classDef x fill:orange',
        'classDef y fill:lightgreen',
        'classDef z fill:lightblue',
        'classDef a fill:#bbb',
    ]
    for line in initial_values_str.splitlines():
        name, value = line.split(': ')
        flowchart.append(f'{name}:::{name[0]}')
    for line in gates_str.splitlines():
        input_str, output = line.split(' -> ')
        input_1, operation, input_2 = input_str.split(' ')
        if output[0] in 'xyz':
            flowchart.append(f'{output}[{operation} {output}]:::{output[0]}')
        else:
            if input_1[0] in 'xyz' and input_2[0] in 'xyz':
                flowchart.append(f'{output}{{{operation} {output}}}:::a')
            else:
                flowchart.append(f'{output}{{{operation} {output}}}')
        flowchart.append(f'{input_1} --> {output}')
        flowchart.append(f'{input_2} --> {output}')

    # go to https://mermaid.live/ and copy paste the content of the variable below
    mermaid_flowchar_definition = '\n'.join(flowchart)

    # confirm the swaps actually work as expected
    fixed_input_data = initial_values_str + '\n\n' + gates_str
    values = simulate(*parse_input(fixed_input_data))
    x, y, z = get_ints(values)
    assert x + y == z

    return ','.join(sorted(c for swap in swaps for c in swap))


if __name__ == '__main__':
    assert part1(EXAMPLE) == 4
    assert part1(EXAMPLE_2) == 2024
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
