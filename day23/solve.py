from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math
# import graphviz

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Vector2:
    x: int
    y: int
    def __neg__(a): return Vector2(-a.x, -a.y)
    def __add__(a, b): return Vector2(a.x + b.x, a.y + b.y)
    def __sub__(a, b): return Vector2(a.x - b.x, a.y - b.y)
    def __mul__(a, s): return Vector2(a.x * s, a.y * s)
    def rotated_ccw(a): return Vector2(a.y, -a.x)
    def abs(a): return Vector2(abs(a.x), abs(a.y))
    def sum(a): return a.x + a.y
    def scaled(a, b): return Vector2(a.x * b.x, a.y * b.y)
    def min(a, b): return Vector2(min(a.x, b.x), min(a.y, b.y))
    def max(a, b): return Vector2(max(a.x, b.x), max(a.y, b.y))

    def __str__(a): return f"({a.x}, {a.y})"
    def __repr__(a): return str(a)

@dataclass
class Grid:
    size: Vector2
    rows: [str]

    def get(self, pos: Vector2) -> str:
        if pos.y < 0 or pos.y >= self.size.y: return "#"
        return self.rows[pos.y][pos.x]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grid_size = Vector2(len(lines[0]), len(lines))

    return Grid(size=grid_size, rows=lines)

# black=30, red=31, green=32, yellow=33, blue=34, magenta=35, cyan=36, white=37 (bg_color=40+)
def colorize(text: str, color: str, bold = False, underline = False, bg_color: str = None) -> str:
    args = [color]
    if bold: args += "1"
    if underline: args += "4"
    if bg_color is not None: args += bg_color
    return f"\033[{';'.join(args)}m{text}\033[0m"

def pretty_format(grid: Grid, intersections: Set[Vector2]):
    result_str = ""
    for y in range(grid.size.y):
        line = ""
        for x in range(grid.size.x):
            pos = Vector2(x, y)
            cell = grid.get(pos)

            if pos in intersections:
                cell = colorize('o' if cell == '.' else cell, "31")

            line += cell
        result_str += line + "\n"
    return result_str

def get_neighbors(pos: Vector2) -> [Vector2]:
    return [pos + offset for offset in [Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1), Vector2(1, 0)]]

def get_cell_dir(cell: str) -> Vector2:
    match cell:
        case "^": return Vector2(0, -1)
        case "<": return Vector2(-1, 0)
        case "v": return Vector2(0, 1)
        case ">": return Vector2(1, 0)
    return None

def do_part1(grid: Grid):
    start_pos = Vector2(grid.rows[0].index("."), 0)
    end_pos = Vector2(grid.rows[-1].index("."), grid.size.y - 1)

    path = {start_pos: (0, None)}
    search_queue = [start_pos]
    while len(search_queue) > 0:
        cur_pos = search_queue.pop(0)
        cur_steps, prev_pos = path[cur_pos]

        if cur_pos == end_pos: continue

        for next_pos in get_neighbors(cur_pos):
            next_cell = grid.get(next_pos)
            if next_pos == prev_pos: continue
            if next_cell == "#": continue
            next_cell_dir = get_cell_dir(grid.get(next_pos))
            if next_cell_dir is not None and next_pos - cur_pos != next_cell_dir: continue

            path[next_pos] = (cur_steps + 1, cur_pos)
            search_queue.append(next_pos)

    print(f"part1: {path[end_pos][0]}")

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Connection:
    start: Vector2
    end: Vector2
    distance: int

def rec_find_connections(grid, intersections, visited, start_pos, cur_pos, distance):
    if cur_pos in intersections:
        return [Connection(start_pos, cur_pos, distance)]

    visited.add(cur_pos)

    connections = []
    for next_pos in get_neighbors(cur_pos):
        if next_pos in visited: continue
        if grid.get(next_pos) == "#": continue
        connections.extend(rec_find_connections(grid, intersections, visited, start_pos, next_pos, distance + 1))

    return connections

# def draw_graph(intersections, connections):
#     dot = graphviz.Graph(comment='The Hike')

#     for intersection in intersections:
#         dot.node(str(intersection), str(intersection))

#     for connection in connections:
#         dot.edge(str(connection.start), str(connection.end), label=str(connection.distance))

#     dot.render('thehike.gv').replace('\\', '/')

def find_longest_path(connections_map, end_node, visited, cur_node):
    if cur_node == end_node: return 0
    visited.add(cur_node)

    max_dist = -99999999
    for dist_to_next, next_node in connections_map[cur_node]:
        if next_node in visited: continue

        dist = dist_to_next + find_longest_path(connections_map, end_node, visited, next_node)
        max_dist = max(max_dist, dist)

    visited.remove(cur_node)
    return max_dist

def do_part2(grid: Grid):
    start_pos = Vector2(grid.rows[0].index("."), 0)
    end_pos = Vector2(grid.rows[-1].index("."), grid.size.y - 1)

    intersections = [start_pos]
    for y in range(1, grid.size.y - 1):
        for x in range(1, grid.size.x - 1):
            pos = Vector2(x, y)
            if grid.get(pos) == "#": continue
            paths_count = len([n for n in get_neighbors(pos) if grid.get(n) != "#"])
            if paths_count > 2: intersections.append(pos)
    intersections.append(end_pos)
    intersections_set = set(intersections)

    connections = []
    visited = set()
    for start in intersections:
        visited.add(start)
        for n_pos in get_neighbors(start):
            if grid.get(n_pos) != "#":
                connections.extend(rec_find_connections(grid, intersections_set, visited, start, n_pos, 1))

    # draw_graph(intersections, connections)

    # with open("map.txt", "w", encoding="utf-8") as outfile:
    #     outfile.write(pretty_format(grid, intersections))

    connections_map = {p: [] for p in intersections}
    for conn in connections:
        connections_map[conn.start].append((conn.distance, conn.end))
        connections_map[conn.end].append((conn.distance, conn.start))

    max_dist = find_longest_path(connections_map, end_pos, set(), start_pos)
    
    print(f"part2: {max_dist}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
