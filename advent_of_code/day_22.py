from collections import defaultdict

from tqdm import tqdm

from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """1
10
100
2024"""

EXAMPLE_2 = """1
2
3
2024"""


def next_secret(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def generate_secrets(secret: int) -> list[int]:
    secrets = [secret]
    for _ in range(2000):
        secrets.append(next_secret(secrets[-1]))
    return secrets


def part1(input_data: str) -> int:
    total = 0
    for line in input_data.splitlines():
        secrets = generate_secrets(int(line))
        total += secrets[-1]
    return total


def part2(input_data: str) -> int:
    changes_to_bananas = defaultdict(int)
    for line in tqdm(input_data.splitlines()):
        secrets = generate_secrets(int(line))
        bananas = [s % 10 for s in secrets]
        diffs = [bananas[i] - bananas[i - 1] for i in range(1, len(bananas))]

        seen_sequences = set()
        for i in range(0, len(bananas) - 4):
            changes = tuple(diffs[i : i + 4])
            if changes not in seen_sequences:
                seen_sequences.add(changes)
                changes_to_bananas[changes] += bananas[i + 4]

    return max(changes_to_bananas.values())


if __name__ == '__main__':
    assert part1(EXAMPLE) == 37327623
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE_2) == 23
    with ContextTimer():
        solution = part2(get_input())
        assert solution > 2216
        print(f'Solution for part 2 is: {solution}')
