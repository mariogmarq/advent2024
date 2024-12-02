const std = @import("std");
const utils = @import("utils.zig");
const day = @import("day02.zig");

const alloc = std.heap.page_allocator;

pub fn main() !void {
    const content = try utils.read_file("input.txt", alloc);
    defer alloc.free(content);

    const sol = try day.part_two(content, alloc);
    std.debug.print("{}", .{sol});
}
