from util.input_util import get_input
from util.timer_util import ContextTimer

EXAMPLE = """2333133121414131402"""


def part1(input_data: str) -> int:
    ints = list(map(int, input_data.strip()))
    file_id_and_lengths = []
    gaps = []
    for i in range(0, len(ints), 2):
        file_id_and_lengths.append([i // 2, ints[i]])
        if i + 1 < len(ints):
            gaps.append(ints[i + 1])

    gaps_reversed = list(reversed(gaps))
    max_position = sum(l for _, l in file_id_and_lengths)
    debug_sequence = []
    checksum = position = 0

    for file_id, amount in file_id_and_lengths:
        for _ in range(amount):
            checksum += position * file_id
            position += 1
            debug_sequence.append(file_id)

        if position >= max_position:
            return checksum

        gap = gaps_reversed.pop()
        while gap > 0:
            amount_to_fill = min(gap, file_id_and_lengths[-1][1])
            gap -= amount_to_fill
            for _ in range(amount_to_fill):
                checksum += position * file_id_and_lengths[-1][0]
                position += 1
                debug_sequence.append(file_id_and_lengths[-1][0])
            file_id_and_lengths[-1][1] -= amount_to_fill
            if file_id_and_lengths[-1][1] <= 0:
                file_id_and_lengths.pop()

    raise Exception("Couldn't fill all gaps")


def part2(input_data: str) -> int:
    ints = list(map(int, input_data.strip()))
    file_id_to_position = []
    file_id_to_length = []
    gap_position_and_lengths = []
    position = 0
    for i in range(0, len(ints), 2):
        file_id_to_length.append(ints[i])
        file_id_to_position.append(position)
        position += ints[i]
        if i + 1 < len(ints):
            gap_position_and_lengths.append([position, ints[i + 1]])
            position += ints[i + 1]

    for file_id in list(reversed(range(1, len(file_id_to_position)))):
        file_length = file_id_to_length[file_id]
        # get the index of the first fitting gap
        gap_index = next(iter(i for i, (_, length) in enumerate(gap_position_and_lengths) if file_length <= length), None)
        if gap_index is not None:
            gap_position, gap_length = gap_position_and_lengths[gap_index]
            if gap_position > file_id_to_position[file_id]:
                # this would be moving the file backwards
                continue
            file_id_to_position[file_id] = gap_position
            if gap_length <= file_length:
                # the gap is completely filled
                # drop it so we don't try to fill this now empty gap
                gap_position_and_lengths.pop(gap_index)
            else:
                # shrink the gap
                gap_position_and_lengths[gap_index][0] += file_length
                gap_position_and_lengths[gap_index][1] -= file_length

    checksum = 0
    for file_id, position in enumerate(file_id_to_position):
        for i in range(file_id_to_length[file_id]):
            checksum += file_id * (position + i)

    return checksum


if __name__ == '__main__':
    assert part1(EXAMPLE) == 1928
    with ContextTimer():
        print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == 2858
    with ContextTimer():
        print(f'Solution for part 2 is: {part2(get_input())}')
