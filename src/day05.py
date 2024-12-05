def read_data():
    with open("input.txt") as f:
        page_orders, updates = f.read().split("\n\n")
        return page_orders.split("\n"), updates.split("\n")


def parse_ordering(page_orders):
    return [
        (int(order.split("|")[0]), int(order.split("|")[1])) for order in page_orders
    ]


def parse_updates(updates):
    return [list(map(int, update.split(","))) for update in updates]


def update_is_in_right_order(update, page_orders):
    already_printed = set()
    for page in update:
        required_pages = [
            order[0] for order in page_orders if order[1] == page and order[0] in update
        ]
        if len(required_pages) > 0:
            if not set(required_pages).issubset(already_printed):
                return False

        already_printed.add(page)

    return True


def part_one():
    page_orders, updates = read_data()
    page_orders = parse_ordering(page_orders)
    updates = parse_updates(updates)
    valid_updates = [
        update for update in updates if update_is_in_right_order(update, page_orders)
    ]
    return sum([update[int(len(update) / 2)] for update in valid_updates])


def find_violated_order(update, page_orders):
    already_printed = set()
    for page in update:
        required_pages = [
            order[0] for order in page_orders if order[1] == page and order[0] in update
        ]
        if len(required_pages) > 0:
            if not set(required_pages).issubset(already_printed):
                return page, required_pages

        already_printed.add(page)

    return None


def part_two():
    page_orders, updates = read_data()
    page_orders = parse_ordering(page_orders)
    updates = parse_updates(updates)
    invalid_updates = [
        update
        for update in updates
        if not update_is_in_right_order(update, page_orders)
    ]

    new_updates = []
    for update in invalid_updates:
        new_update = update.copy()
        violated_order = find_violated_order(new_update, page_orders)
        while violated_order is not None:
            page_failed, required_pages = violated_order
            index_of_page_failed = new_update.index(page_failed)
            indexes_of_required = max(
                [new_update.index(page) for page in required_pages]
            )
            new_update.pop(index_of_page_failed)
            new_update.insert(indexes_of_required + 1, page_failed)
            violated_order = find_violated_order(new_update, page_orders)

        new_updates.append(new_update)

    return sum([update[int(len(update) / 2)] for update in new_updates])


if __name__ == "__main__":
    print(part_one())
    print(part_two())
