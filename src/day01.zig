const std = @import("std");

pub fn part_one(numbers: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    var first_list = std.ArrayList(i32).init(alloc);
    var second_list = std.ArrayList(i32).init(alloc);
    defer first_list.deinit();
    defer second_list.deinit();

    var lines = std.mem.tokenize(u8, numbers, "\n");
    while (lines.next()) |line| {
        var numbers_iterator = std.mem.splitSequence(u8, line, "   ");
        const first = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);
        const second = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);

        try first_list.append(first);
        try second_list.append(second);
    }

    std.mem.sort(i32, first_list.items, {}, comptime std.sort.asc(i32));
    std.mem.sort(i32, second_list.items, {}, comptime std.sort.asc(i32));

    var total_distance = @as(i32, 0);
    for (first_list.items, second_list.items) |a, b| {
        total_distance += (a - b) * std.math.sign(a - b);
    }

    return total_distance;
}

pub fn part_two(numbers: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    var first_list = std.ArrayList(i32).init(alloc);
    var second_list = std.ArrayList(i32).init(alloc);
    defer first_list.deinit();
    defer second_list.deinit();

    var lines = std.mem.tokenize(u8, numbers, "\n");
    while (lines.next()) |line| {
        var numbers_iterator = std.mem.splitSequence(u8, line, "   ");
        const first = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);
        const second = try std.fmt.parseInt(i32, numbers_iterator.next().?, 10);

        try first_list.append(first);
        try second_list.append(second);
    }

    var similarity_score = std.AutoHashMap(i32, i32).init(alloc);
    defer similarity_score.deinit();
    for (second_list.items) |num| {
        if (similarity_score.contains(num)) {
            try similarity_score.put(num, similarity_score.get(num).? + 1);
        } else {
            try similarity_score.put(num, @as(u32, 1));
        }
    }

    var score = @as(i32, 0);
    for (first_list.items) |num| {
        const similarity = similarity_score.get(num) orelse 0;
        score += similarity * num;
    }

    return score;
}
