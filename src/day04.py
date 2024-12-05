import numpy as np


def read_file():
    with open("input.txt") as f:
        return [x for x in f.read().split("\n") if x]


def word_is_xmas(s):
    return "xmas" == s.lower() or "xmas" == s.lower()[::-1]


def search_horizontal(inp):
    horizontal = 0
    for line in inp:
        horizontal += sum([word_is_xmas(line[i : i + 4]) for i in range(len(line) - 3)])
    return horizontal


def part_one(inp):
    horizontal = search_horizontal(inp)

    transpose = list(zip(*inp))
    transpose = ["".join(x) for x in transpose]
    vertical = search_horizontal(transpose)

    matrix = np.array([list(x) for x in inp])
    height, width = matrix.shape
    diagonals = [matrix.diagonal(i) for i in range(-height, width)]
    diagonals = [x for x in diagonals if len(x) >= 4]
    diagonals = ["".join(x) for x in diagonals]
    diagonal = search_horizontal(diagonals)

    second_diagonals = [matrix[::-1, :].diagonal(i) for i in range(-height, width)]
    second_diagonals = [x for x in second_diagonals if len(x) >= 4]
    second_diagonals = ["".join(x) for x in second_diagonals]
    second_diagonal = search_horizontal(second_diagonals)

    return horizontal + vertical + diagonal + second_diagonal


def is_x_mas(m):
    first_diagonal = np.diagonal(m)
    first_diagonal = "".join(first_diagonal)
    second_diagonal = np.diagonal(m[::-1])
    second_diagonal = "".join(second_diagonal)
    return (first_diagonal == "MAS" or first_diagonal == "SAM") and (
        second_diagonal == "MAS" or second_diagonal == "SAM"
    )


def part_two(inp):
    matrix = np.array([list(x) for x in inp])
    sliding = np.lib.stride_tricks.sliding_window_view(matrix, (3, 3)).reshape(-1, 3, 3)

    return sum([is_x_mas(x) for x in sliding])


if __name__ == "__main__":
    content = read_file()
    print(part_two(content))
