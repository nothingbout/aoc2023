from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False

INPUT_FILE = "example2_4.txt" if IS_EXAMPLE else "input.txt"

def v_check(a, b):
    if isinstance(b, tuple):
        if len(a) != len(b): raise Exception(f"length mismatch: len(a) == {len(a)}, len(b) == {len(b)}")
        return True
    return False
def v_add(a, b): return tuple(map(lambda x, y: x + y, a, b)) if v_check(a, b) else tuple(map(lambda x: x + b, a))
def v_sub(a, b): return tuple(map(lambda x, y: x - y, a, b)) if v_check(a, b) else tuple(map(lambda x: x - b, a))

def v_turn_cw(a): return (-a[1], a[0])
def v_turn_ccw(a): return (a[1], -a[0])

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    return lines

def get_connected_offsets(tile):
    match tile:
        case '|': offsets = ((0, -1), (0, 1))
        case '-': offsets = ((-1, 0), (1, 0))
        case 'L': offsets = ((0, -1), (1, 0))
        case 'J': offsets = ((-1, 0), (0, -1))
        case '7': offsets = ((-1, 0), (0, 1))
        case 'F': offsets = ((1, 0), (0, 1))
        case _: offsets = None
    return offsets

def get_map_dims(map):
    return (len(map[0]), len(map))

def get_map_tile(map, pos):
    x, y = pos
    w, h = get_map_dims(map)
    if x < 0 or x >= w or y < 0 or y >= h: return None
    return map[y][x]

def get_connected_neighbors(map, pos):
    neighbors = []
    offsets = get_connected_offsets(get_map_tile(map, pos))
    if offsets is None: return neighbors
    for offset in offsets:
        n_pos = v_add(pos, offset)
        tile = get_map_tile(map, n_pos)
        if tile is not None:
            neighbors.append(n_pos)
    return neighbors

def get_start_pos(map):
    map_w, map_h = get_map_dims(map)
    start_pos = None
    for y in range(0, map_h):
        for x in range(0, map_w):
            if get_map_tile(map, (x, y)) == 'S':
                start_pos = (x, y)
    return start_pos

def get_loop_edges(map, start_pos):
    start_edges = []
    for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        n_pos = v_add(start_pos, offset)
        if start_pos in get_connected_neighbors(map, n_pos):
            start_edges.append((start_pos, n_pos, 1))

    loop_edges = start_edges
    while True:
        next_edges = []
        for prev_pos, cur_pos, cur_steps in loop_edges[-2:]:
            neighbors = get_connected_neighbors(map, cur_pos)
            next_pos = None
            for neighbor in neighbors:
                if neighbor != prev_pos:
                    next_pos = neighbor
            loop_edges.append((cur_pos, next_pos, cur_steps + 1))

        if loop_edges[-2][1] == loop_edges[-1][1]:
            break
    return loop_edges

def do_part1(map):
    start_pos = get_start_pos(map)
    loop_edges = get_loop_edges(map, start_pos)
    print(f"part1: {loop_edges[-1][2]}")

def do_part2(map):
    start_pos = get_start_pos(map)
    loop_edges = get_loop_edges(map, start_pos)
    loop_points = [start_pos] + [e[1] for e in loop_edges[::2] + list(reversed(loop_edges[1::2]))]

    total_turn = 0
    for i in range(0, len(loop_points)):
        p0 = loop_points[i - 1] if i - 1 >= 0 else loop_points[-1]
        p1 = loop_points[i]
        p2 = loop_points[i + 1] if i + 1 < len(loop_points) else loop_points[0]
        d1 = v_sub(p1, p0)
        d2 = v_sub(p2, p1)
        if v_turn_ccw(d1) == d2: total_turn -= 1
        elif v_turn_cw(d1) == d2: total_turn += 1

    # force ccw
    if total_turn > 0:
        loop_points = list(reversed(loop_points))

    def floodfill(p, points_at_or_in_loop):
        points_at_or_in_loop.add(p)
        for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            n_pos = v_add(p, offset)
            if n_pos in points_at_or_in_loop: continue
            floodfill(n_pos, points_at_or_in_loop)

    loop_points_set = set(loop_points)
    points_at_or_in_loop = loop_points_set.copy()
    for i in range(0, len(loop_points)):
        p1 = loop_points[i]
        p2 = loop_points[i + 1] if i + 1 < len(loop_points) else loop_points[0]
        d1 = v_sub(p2, p1)
        dn = v_turn_ccw(d1)
        ips = [v_add(p1, dn), v_add(p2, dn)]
        for ip in ips:
            if not ip in points_at_or_in_loop:
                floodfill(ip, points_at_or_in_loop)

    inner_points = points_at_or_in_loop - loop_points_set

    # map_w, map_h = get_map_dims(map)
    # for y in range(0, map_h):
    #     line = ""
    #     for x in range(0, map_w):
    #         p = (x, y)
    #         c = '.'
    #         if p in loop_points_set: c = '*'
    #         elif p in inner_points: c = 'I'
    #         line += c
    #     print(line)

    print(f"part2: {len(inner_points)}")

start_time = datetime.now()
input_lines = parse_input()

do_part1(input_lines)
do_part2(input_lines)

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
