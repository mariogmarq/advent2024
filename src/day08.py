from typing import List
from queue import Queue
import numpy as np
from functools import reduce


def read_input():
    with open("input.txt") as f:
        return [line for line in f.read().split("\n") if line]


def compute_antinodes(first_antena: np.ndarray, second_antena: np.ndarray):
    assert first_antena.shape == second_antena.shape == (2,)
    y_diff = first_antena[0] - second_antena[0]
    x_diff = first_antena[1] - second_antena[1]

    first_antinode = (first_antena[0] + y_diff, first_antena[1] + x_diff)
    second_antinode = (second_antena[0] - y_diff, second_antena[1] - x_diff)

    return first_antinode, second_antinode


def compute_all_antinodes(antena_pos: np.ndarray, matrix_shape: tuple):
    antinodes = set()
    for i in range(antena_pos.shape[0]):
        for j in range(i + 1, antena_pos.shape[0]):
            first_antinode, second_antinode = compute_antinodes(
                antena_pos[i], antena_pos[j]
            )
            if (
                0 <= first_antinode[0] < matrix_shape[0]
                and 0 <= first_antinode[1] < matrix_shape[1]
            ):
                antinodes.add(first_antinode)
            if (
                0 <= second_antinode[0] < matrix_shape[0]
                and 0 <= second_antinode[1] < matrix_shape[1]
            ):
                antinodes.add(second_antinode)

    return antinodes


def part_one(s: List[str]):
    kinds_of_antenas = {a for a in "".join(s) if a.isalnum()}
    matrix = np.array([[a for a in line] for line in s])
    antena_pos = {antena: np.argwhere(matrix == antena) for antena in kinds_of_antenas}
    antinodes = {
        antena: compute_all_antinodes(antena_pos[antena], matrix.shape)
        for antena in kinds_of_antenas
    }

    unique_antinodes = reduce(lambda x, y: x.union(y), antinodes.values())

    return len(unique_antinodes)


def compute_antinodes_part_two(
    first_antena: np.ndarray, second_antena: np.ndarray, matrix_shape: tuple
):
    assert first_antena.shape == second_antena.shape == (2,)
    y_diff = first_antena[0] - second_antena[0]
    x_diff = first_antena[1] - second_antena[1]

    first_antinodes = []
    second_antinodes = []

    x_first = first_antena[1] + x_diff
    y_first = first_antena[0] + y_diff
    while 0 <= x_first < matrix_shape[1] and 0 <= y_first < matrix_shape[0]:
        first_antinodes.append((y_first, x_first))
        x_first += x_diff
        y_first += y_diff

    x_second = second_antena[1] - x_diff
    y_second = second_antena[0] - y_diff
    while 0 <= x_second < matrix_shape[1] and 0 <= y_second < matrix_shape[0]:
        second_antinodes.append((y_second, x_second))
        x_second -= x_diff
        y_second -= y_diff

    return first_antinodes + second_antinodes


def compute_all_antinodes_part_two(antena_pos: np.ndarray, matrix_shape: tuple):
    unique_antinodes = set()
    for i in range(antena_pos.shape[0]):
        for j in range(i + 1, antena_pos.shape[0]):
            antinodes = compute_antinodes_part_two(
                antena_pos[i], antena_pos[j], matrix_shape
            )
            for antinode in [
                antinode
                for antinode in antinodes
                if matrix_shape[0] > antinode[0] >= 0
                and matrix_shape[1] > antinode[1] >= 0
            ]:
                unique_antinodes.add(antinode)

    if antena_pos.shape[0] > 1:
        for pos in antena_pos:
            unique_antinodes.add((pos[0], pos[1]))

    return unique_antinodes


def part_two(s: List[str]):
    kinds_of_antenas = {a for a in "".join(s) if a.isalnum()}
    matrix = np.array([[a for a in line] for line in s])
    antena_pos = {antena: np.argwhere(matrix == antena) for antena in kinds_of_antenas}
    antinodes = {
        antena: compute_all_antinodes_part_two(antena_pos[antena], matrix.shape)
        for antena in kinds_of_antenas
    }

    unique_antinodes = reduce(lambda x, y: x.union(y), antinodes.values())

    return len(unique_antinodes)


if __name__ == "__main__":
    print(part_one(read_input()))
    print(part_two(read_input()))
