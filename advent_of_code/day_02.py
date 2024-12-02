from util.input_util import get_input

EXAMPLE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def report_is_safe(report: list[int], can_remove: bool) -> bool:
    # Instead of looking at the numbers, we'll always look at the differences between the numbers
    diffs = [report[i] - report[i - 1] for i in range(1, len(report))]

    if diffs_are_fine(diffs):
        return True

    if can_remove:
        if diffs_are_fine(diffs[1:]) or diffs_are_fine(diffs[:-1]):
            # Try dropping the first one or the last one
            return True

        if len(set(report)) + 2 <= len(report):
            # At least 2 duplicates, can't be solved by dropping 1 of the duplicates
            return False

        if sum([d < 0 for d in diffs]) >= 2 and sum([d > 0 for d in diffs]) >= 2:
            # If there are multiple positives and multiple negatives, that also can't be fixed by dropping 1 of them
            return False

        for i in range(1, len(diffs)):
            # Combine 2 subsequent diffs. This corresponds by removing a single number
            adjusted = diffs[: i - 1] + [diffs[i - 1] + diffs[i]] + diffs[i + 1 :]
            if diffs_are_fine(adjusted):
                return True

    return False


def diffs_are_fine(diffs: list[int]) -> bool:
    return all(1 <= diff <= 3 for diff in diffs) or all(-3 <= diff <= -1 for diff in diffs)


def part1(input_data: str) -> int:
    reports = [[int(i) for i in line.split()] for line in input_data.splitlines()]
    return sum(report_is_safe(report, can_remove=False) for report in reports)


def part2(input_data: str) -> int:
    reports = [[int(i) for i in line.split()] for line in input_data.splitlines()]
    return sum(report_is_safe(report, can_remove=True) for report in reports)


if __name__ == '__main__':
    assert part1(EXAMPLE) == 2
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 4
    assert report_is_safe([26, 31, 32, 34, 37, 39], True)
    assert report_is_safe([88, 87, 85, 88, 82], True)
    assert report_is_safe([1, 2, 3, 4, 100], True)
    assert report_is_safe([1, 100], True)
    assert report_is_safe([1, 100, 3], True)
    assert report_is_safe([100, 1, 3], True)
    print(f'Solution for part 2 is: {part2(get_input())}')
