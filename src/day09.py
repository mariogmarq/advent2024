from typing import List


def read_input():
    with open("input.txt") as f:
        return [int(num) for num in f.read().strip()]


def create_ids(input: List[int]):
    return [(i, val) for i, val in enumerate(input[::2])]


def compute_free_space(input: List[int]):
    return [i for i in input[1::2]]


def sort_disk(free_space, ids):
    new_disk = [ids[0]]

    current_free_index = 0
    current_ids_index = len(ids) - 1
    ids_index_already_used = 0

    while current_ids_index > ids_index_already_used:
        _, size = ids[current_ids_index]
        free_size = free_space[current_free_index]
        if size <= free_size:
            new_disk.append(ids[current_ids_index])
            free_space[current_free_index] -= size
            current_ids_index -= 1
            continue

        total_space_i_can_put = free_size
        ids[current_ids_index] = (
            ids[current_ids_index][0],
            size - total_space_i_can_put,
        )
        new_disk.append((ids[current_ids_index][0], total_space_i_can_put))
        current_free_index += 1
        ids_index_already_used += 1
        new_disk.append(ids[ids_index_already_used])

    new_disk = [(i, val) for i, val in new_disk if val != 0]
    return new_disk


def compute_check_sum(new_disk):
    current_index = 0
    checksum = 0
    for index, ammount in new_disk:
        first_id = current_index
        last_id = current_index + ammount - 1
        sum_of_ids = ((first_id + last_id) / 2) * ammount
        checksum += int(sum_of_ids) * index

        current_index += ammount

    return checksum


def part_one(input: List[int]):
    free_space = compute_free_space(input)
    ids = create_ids(input)
    new_disk = sort_disk(free_space.copy(), ids.copy())
    return compute_check_sum(new_disk)


def sort_disk_part_two(disklayout: List[tuple]):
    new_layout = disklayout.copy()

    used_disk_indices = [i for i, (_, _, is_used) in enumerate(new_layout) if is_used]

    current_disk_index = len(used_disk_indices) - 1
    while current_disk_index > 0:
        # Get current file
        current_file = new_layout[used_disk_indices[current_disk_index]]
        index, size, is_used = current_file
        assert is_used

        # Get the first free space that can fit the file
        free_space_index = -1
        for i, (_, free_space, is_used) in enumerate(new_layout):
            # Only check spaces to the left
            if i >= used_disk_indices[current_disk_index]:
                break

            # If the space is not used and can fit the file
            if not is_used and size <= free_space:
                free_space_index = i
                break

        # No free space found, move to next file
        if free_space_index == -1:
            current_disk_index -= 1
            continue

        free_space = new_layout[free_space_index]
        _, free_size, _ = free_space
        # The current file position becomes free space
        new_layout[used_disk_indices[current_disk_index]] = (
            0,
            size,
            False,
        )
        # We resize the free space found and insert the file
        new_layout[free_space_index] = (0, free_size - size, False)
        new_layout.insert(free_space_index, (index, size, True))
        used_disk_indices = [
            i for i, (_, _, is_used) in enumerate(new_layout) if is_used
        ]

    new_layout = [(i, val) for i, val, _ in new_layout if val > 0]

    return new_layout


def part_two(input: List[int]):
    free_space = compute_free_space(input)
    ids = create_ids(input)
    disk_layout = [(ids[0][0], ids[0][1], True)]
    for (i, size), free in zip(ids[1:], free_space):
        disk_layout.append((0, free, False))
        disk_layout.append((i, size, True))

    new_disk = sort_disk_part_two(disk_layout)
    return compute_check_sum(new_disk)


if __name__ == "__main__":
    print(part_one(read_input()))
    print(part_two(read_input()))
