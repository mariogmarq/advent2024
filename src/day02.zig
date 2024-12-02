const std = @import("std");

fn report_is_safe(numbers: []const i32) anyerror!bool {
    var is_safe = true;
    var previous_number: ?i32 = null;
    var decreasing: ?bool = null;

    for (numbers) |num| {
        if (previous_number == null) {
            previous_number = num;
            continue;
        }

        if (decreasing == null) {
            decreasing = previous_number.? > num;
        }

        if ((previous_number.? > num) != decreasing.?) {
            is_safe = false;
        }

        if (((previous_number.? - num) * std.math.sign(previous_number.? - num)) > 3 or ((previous_number.? - num) == 0)) {
            is_safe = false;
        }

        previous_number = num;
    }

    return is_safe;
}

pub fn part_one(content: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    var lines = std.mem.tokenize(u8, content, "\n");
    var safe = @as(i32, 0);
    while (lines.next()) |line| {
        var numbers = std.mem.tokenize(u8, line, " ");

        var arr = std.ArrayList(i32).init(alloc);
        defer arr.deinit();

        while (numbers.next()) |number| {
            const num = try std.fmt.parseInt(i32, number, 10);
            try arr.append(num);
        }

        if (try report_is_safe(arr.items)) {
            safe += 1;
        }
    }

    return safe;
}

pub fn part_two(content: []u8, alloc: std.mem.Allocator) anyerror!i32 {
    var lines = std.mem.tokenize(u8, content, "\n");
    var safe = @as(i32, 0);
    while (lines.next()) |line| {
        var numbers = std.mem.tokenize(u8, line, " ");
        var arr = std.ArrayList(i32).init(alloc);
        defer arr.deinit();

        while (numbers.next()) |number| {
            const num = try std.fmt.parseInt(i32, number, 10);
            try arr.append(num);
        }

        var is_safe = try report_is_safe(arr.items);
        for (0..arr.items.len) |i| {
            var new_report = try arr.clone();
            defer new_report.deinit();

            _ = new_report.orderedRemove(i);

            is_safe = is_safe or (try report_is_safe(new_report.items));
        }

        if (is_safe) {
            safe += 1;
        }
    }

    return safe;
}
