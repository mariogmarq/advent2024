const std = @import("std");
const utils = @import("utils.zig");
const day1 = @import("day01.zig");

const alloc = std.heap.page_allocator;

pub fn main() !void {
    const content = try utils.read_file("input.txt", alloc);
    defer alloc.free(content);

    const sol = try day1.part_two(content, alloc);
    std.debug.print("{}", .{sol});
}
