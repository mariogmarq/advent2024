from typing import List
from tqdm import tqdm


def read_input():
    with open("new_input.txt") as f:
        return [line for line in f.read().split("\n") if line]


GUARD = "^"
OBSTACKLE = "#"


def rotate_90(dir: List[int]):
    match dir:
        case [-1, 0]:
            return [0, 1]
        case [0, 1]:
            return [1, 0]
        case [1, 0]:
            return [0, -1]
        case [0, -1]:
            return [-1, 0]
        case _:
            raise ValueError()


def find_path(s):
    positions = []
    dir = [-1, 0]

    row = [i for i, line in enumerate(s) if GUARD in line][0]
    col = s[row].index(GUARD)

    height = len(s)
    width = len(s[0])

    while 0 <= row < height and 0 <= col < width:
        if (row, col, dir) in positions:
            return positions, True

        positions.append((row, col, dir))
        next_row = row + dir[0]
        next_col = col + dir[1]
        if 0 <= next_row < height and 0 <= next_col < width:
            if s[next_row][next_col] == OBSTACKLE:
                dir = rotate_90(dir)
                continue

        row += dir[0]
        col += dir[1]

    return positions, False


def part_one(s: List[str]):
    path, _ = find_path(s)
    return len(set([(row, col) for row, col, _ in path]))


def part_two_optimized(s):
    path, _ = find_path(s)
    loops = 0

    for i, pos in enumerate(path):
        row, col, dir = pos
        new_dir = rotate_90(dir)
        possible_positions = []

        while 0 <= row < len(s) and 0 <= col < len(s[0]):
            possible_positions.append((row, col, new_dir))
            row = row + new_dir[0]
            col = col + new_dir[1]

        if any([p_pos in path[:i] for p_pos in possible_positions]):
            loops += 1

    return loops


def part_two(s: List[str]):
    height = len(s)
    width = len(s[0])

    loops = 0

    for i in tqdm(range(height)):
        for j in range(width):
            if s[i][j] == OBSTACKLE or s[i][j] == GUARD:
                continue
            new_s = s.copy()
            new_s[i] = new_s[i][:j] + OBSTACKLE + new_s[i][j + 1 :]
            _, loop = find_path(new_s)
            loops += 1 if loop else 0

    return loops


if __name__ == "__main__":
    print(part_one(read_input()))
    print(part_two_optimized(read_input()))
    # print(part_two(read_input()))
