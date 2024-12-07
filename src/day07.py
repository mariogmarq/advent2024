def read_input():
    with open("input.txt") as f:
        lines = [line for line in f.read().split("\n") if line]

    input = []
    for line in lines:
        result, operands = line.split(": ")
        input.append((int(result), [int(operand) for operand in operands.split(" ")]))

    return input


def input_is_feasible(result, operands):
    if len(operands) == 1:
        return result == operands[0]
    if result < operands[0]:
        return False

    feasible_by_sum = input_is_feasible(
        result, [operands[0] + operands[1]] + operands[2:]
    )
    feasible_by_product = input_is_feasible(
        result, [operands[0] * operands[1]] + operands[2:]
    )

    return feasible_by_sum or feasible_by_product


def part_one(s):
    return sum(
        [result for result, operands in s if input_is_feasible(result, operands)]
    )


def input_is_feasible_two(result, operands):
    if len(operands) == 1:
        return result == operands[0]
    if result < operands[0]:
        return False

    feasible_by_sum = input_is_feasible_two(
        result, [operands[0] + operands[1]] + operands[2:]
    )
    feasible_by_product = input_is_feasible_two(
        result, [operands[0] * operands[1]] + operands[2:]
    )

    feasible_by_concatenation = input_is_feasible_two(
        result, [int(f"{operands[0]}{operands[1]}")] + operands[2:]
    )

    return feasible_by_sum or feasible_by_product or feasible_by_concatenation


def part_two(s):
    return sum(
        [result for result, operands in s if input_is_feasible_two(result, operands)]
    )


if __name__ == "__main__":
    input = read_input()
    print(part_one(input))
    print(part_two(input))
