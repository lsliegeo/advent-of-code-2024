from collections import defaultdict

from util.input_util import get_input

EXAMPLE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def update_is_valid(update: tuple[int], page_before_to_pages_after: dict[int, set[int]]) -> bool:
    pages_seen = set()
    for page in update:
        if pages_seen & page_before_to_pages_after[page]:
            return False
        pages_seen.add(page)
    return True


def part1(input_data: str) -> int:
    page_ordering_rules, updates = input_data.split('\n\n')
    page_ordering_rules = [tuple(map(int, line.split('|'))) for line in page_ordering_rules.splitlines()]
    updates = [tuple(map(int, line.split(','))) for line in updates.splitlines()]

    page_before_to_pages_after = defaultdict(set)
    for before, after in page_ordering_rules:
        page_before_to_pages_after[before].add(after)

    total = 0
    for update in updates:
        if update_is_valid(update, page_before_to_pages_after):
            total += update[len(update) // 2]

    return total


def part2(input_data: str) -> int:
    page_ordering_rules, updates = input_data.split('\n\n')
    page_ordering_rules = [tuple(map(int, line.split('|'))) for line in page_ordering_rules.splitlines()]
    updates = [tuple(map(int, line.split(','))) for line in updates.splitlines()]

    page_before_to_pages_after = defaultdict(set)
    for before, after in page_ordering_rules:
        page_before_to_pages_after[before].add(after)

    total = 0
    for update in updates:
        if not update_is_valid(update, page_before_to_pages_after):
            fixed_update = fix_order(update, page_before_to_pages_after)
            total += fixed_update[len(fixed_update) // 2]

    return total


def fix_order(update: tuple[int], page_before_to_pages_after: dict[int, set[int]]) -> list[int]:
    page_before_to_pages_after = {k: v & set(update) for k, v in page_before_to_pages_after.items() if k in update}
    return sorted(update, key=lambda page: -len(page_before_to_pages_after[page]))


if __name__ == '__main__':
    assert part1(EXAMPLE) == 143
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 123
    print(f'Solution for part 2 is: {part2(get_input())}')
