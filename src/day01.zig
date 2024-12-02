const std = @import("std");

fn read_lists(numbers: []u8, alloc: std.mem.Allocator) anyerror![2]std.ArrayList(i32) {
    var first_list = std.ArrayList(i32).init(alloc);
    var second_list = std.ArrayList(i32).init(alloc);

    var lines = std.mem.tokenize(u8, numbers, "\n");
    while (lines.next()) |line| {
        var numbers_iterator = std.mem.splitSequence(u8, line, "   ");
        const first = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);
        const second = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);

        try first_list.append(first);
        try second_list.append(second);
    }

    return [_]std.ArrayList(i32){ first_list, second_list };
}

pub fn part_one(numbers: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    const lists = try read_lists(numbers, alloc);
    var first_list = lists[0];
    var second_list = lists[1];
    defer first_list.deinit();
    defer second_list.deinit();

    std.mem.sort(i32, first_list.items, {}, comptime std.sort.asc(i32));
    std.mem.sort(i32, second_list.items, {}, comptime std.sort.asc(i32));

    var total_distance = @as(i32, 0);
    for (first_list.items, second_list.items) |a, b| {
        total_distance += @abs(a - b);
    }

    return total_distance;
}

pub fn create_counter(comptime T: type, values: []const T, alloc: std.mem.Allocator) !std.AutoHashMap(T, i32) {
    var counter = std.AutoHashMap(T, i32).init(alloc);
    for (values) |value| {
        const times_appeared = counter.get(value) orelse 0;
        try counter.put(value, times_appeared + 1);
    }

    return counter;
}

pub fn part_two(numbers: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    const lists = try read_lists(numbers, alloc);
    var first_list = lists[0];
    var second_list = lists[1];
    defer first_list.deinit();
    defer second_list.deinit();

    var similarity_score = try create_counter(i32, second_list.items, alloc);
    defer similarity_score.deinit();

    var score = @as(i32, 0);
    for (first_list.items) |num| {
        const similarity = similarity_score.get(num) orelse 0;
        score += similarity * num;
    }

    return score;
}
