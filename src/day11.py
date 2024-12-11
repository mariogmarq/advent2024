from typing import List
from collections import Counter
from tqdm import tqdm


def read_input():
    with open("input.txt") as f:
        return f.read().strip().split(" ")


def blink(stones: List[str]) -> List[str]:
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif len(stone) % 2 == 0:
            first_half = stone[: len(stone) // 2]
            second_half = stone[len(stone) // 2 :]
            new_stones.extend([f"{int(first_half)}", f"{int(second_half)}"])
        else:
            new_stones.append(f"{int(stone)*2024}")
    return new_stones


def part_one(s):
    stones = s.copy()
    for _ in tqdm(range(25)):
        stones = blink(stones)
    return len(stones)


def part_two(s):
    # Since order doesnt matter, we can just do a counter and update it each step
    stones = Counter(s)
    for _ in range(75):
        new_counter = Counter()
        for stone, count in stones.items():
            if stone == "0":
                new_counter["1"] += count
            elif len(stone) % 2 == 0:
                first_half = stone[: len(stone) // 2]
                second_half = stone[len(stone) // 2 :]
                new_counter[f"{int(first_half)}"] += count
                new_counter[f"{int(second_half)}"] += count
            else:
                new_counter[f"{int(stone)*2024}"] += count
        stones = new_counter

    return sum(stones.values())


if __name__ == "__main__":
    s = read_input()
    print(part_one(s))
    print(part_two(s))
