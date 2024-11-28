const std = @import("std");

pub fn read_file(file_name: []const u8, allocator: std.mem.Allocator) anyerror![]u8 {
    var path_buffer: [std.fs.MAX_PATH_BYTES]u8 = undefined;
    const real_path = try std.fs.realpath(file_name, &path_buffer);

    const file = try std.fs.openFileAbsolute(real_path, .{});
    defer file.close();
    var br = std.io.bufferedReader(file.reader());
    const reader = br.reader();

    const content = try reader.readAllAlloc(allocator, std.math.maxInt(usize));
    return content;
}
