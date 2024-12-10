import numpy as np


def read_input():
    with open("input.txt") as f:
        s = [[int(l) for l in line] for line in f.read().split("\n")]
    return np.array(s)


def position_is_reachable(s: np.ndarray, start: tuple, end: tuple, visited=None):
    # I know I could do something like A* but backtracking is enough here
    if visited is None:
        visited = set()

    if start == end:
        return True
    visited.add(start)
    # Generate next moves
    axis = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for a in axis:
        new_pos = (start[0] + a[0], start[1] + a[1])
        if (
            0 <= new_pos[0] < s.shape[0]
            and 0 <= new_pos[1] < s.shape[1]
            and tuple(new_pos) not in visited
        ):
            if s[new_pos] == s[start] + 1:
                if position_is_reachable(s, new_pos, end, visited):
                    return True

    return False


def part_one(s):
    zeroes = np.argwhere(s == 0)
    nines = np.argwhere(s == 9)
    grades = []
    for z in zeroes:
        grades += [position_is_reachable(s, tuple(z), tuple(n), None) for n in nines]

    return sum(grades)


def find_all_paths(s: np.ndarray, start: tuple, end: tuple):
    if start == end:
        return 1  # There is only one path from one point to itself
    # Generate next moves
    axis = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    paths = 0
    for ax in axis:
        new_pos = (start[0] + ax[0], start[1] + ax[1])
        if (
            0 <= new_pos[0] < s.shape[0]
            and 0 <= new_pos[1] < s.shape[1]
            and s[new_pos] == s[start] + 1
        ):
            paths += find_all_paths(s, new_pos, end)

    return paths


def part_two(s):
    zeroes = np.argwhere(s == 0)
    nines = np.argwhere(s == 9)
    grades = 0
    for z in zeroes:
        grades += sum([find_all_paths(s, tuple(z), tuple(n)) for n in nines])

    return grades


if __name__ == "__main__":
    print(part_one(read_input()))
    print(part_two(read_input()))
