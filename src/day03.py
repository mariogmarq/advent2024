# Zig doesnt have regex xdddd
import re

test_str = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def read_file():
    with open("input.txt") as f:
        return f.read()


def part_one(s):
    pattern = re.compile(r"mul\((\d+,\d+)\)")
    finds = pattern.findall(s)
    nums = [int(x.split(",")[0]) * int(x.split(",")[1]) for x in finds]
    return sum(nums)


def part_two(s):
    pattern = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    finds = pattern.findall(s)
    enabled = True
    sum = 0
    for find in finds:
        if find == "do()":
            enabled = True
            continue
        if find == "don't()":
            enabled = False
            continue
        if enabled:
            lh, rh = find.split(",")
            lh, rh = int(lh[4:]), int(rh[:-1])
            sum += lh * rh

    return sum


if __name__ == "__main__":
    print(part_two(read_file()))
