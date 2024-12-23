from collections import defaultdict

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def parse_input(input_data: str) -> dict[str, set[str]]:
    vertices = defaultdict(set)
    for line in input_data.splitlines():
        a, b = line.split('-')
        vertices[a].add(b)
        vertices[b].add(a)
    return vertices


def part1(input_data: str) -> int:
    vertices = parse_input(input_data)
    nodes = sorted(vertices)
    nodes_with_t = sorted(node for node in nodes if node[0] == 't')

    valid_combinations = set()
    for t in nodes_with_t:
        for a in vertices[t]:
            for b in vertices[t] & vertices[a]:
                valid_combinations.add(tuple(sorted([t, a, b])))

    return len(valid_combinations)


def bron_kerbosh(r: set[str], p: set[str], x: set[str], vertices: dict[str, set[str]], result: list):
    if not p and not x:
        if len(r) > len(result[0]):
            result[0] = tuple(r)
    while p:
        vertex = p.pop()
        bron_kerbosh(r | {vertex}, p & vertices[vertex], x & vertices[vertex], vertices, result)
        x.add(vertex)


def part2(input_data: str) -> str:
    vertices = parse_input(input_data)
    result = [[]]
    bron_kerbosh(set(), set(vertices), set(), vertices, result)
    return ','.join(sorted(result[0]))


if __name__ == '__main__':
    assert part1(EXAMPLE) == 7
    with ContextTimer():
        solution = part1(get_input())
        assert solution > 437
        assert solution < 2308
        print(f'Solution for part 1 is: {solution}')

    assert part2(EXAMPLE) == 'co,de,ka,ta'
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
