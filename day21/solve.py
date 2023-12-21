from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math

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
class InputData:
    grid_size: Vector2
    start_pos: Vector2
    rows: [str]

    def get(self, pos: Vector2) -> str:
        return self.rows[pos.y][pos.x]
    
    def in_bounds(self, pos: Vector2) -> bool:
        if pos.x < 0 or pos.x >= self.grid_size.x: return False
        if pos.y < 0 or pos.y >= self.grid_size.y: return False
        return True
    
    def wrap(self, pos: Vector2) -> Vector2:
        return Vector2(pos.x % self.grid_size.x, pos.y % self.grid_size.y)

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grid_size = Vector2(len(lines[0]), len(lines))
    rows = []

    for y, line in enumerate(lines):
        x = line.find("S")
        if x >= 0:
            start_pos = Vector2(x, y)
            rows.append(line[:x] + "." + line[x + 1:])
        else:
            rows.append(line)
        
    return InputData(grid_size=grid_size, start_pos=start_pos, rows=rows)

def get_neighbors(pos: Vector2) -> [Vector2]:
    return [pos + offset for offset in [Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1), Vector2(1, 0)]]

def pretty_format(input_data: InputData, positions: Set[Vector2], draw_bounds: (Vector2, Vector2)):
    bounds_min, bounds_max = draw_bounds
    result_str = ""
    grid_size = input_data.grid_size
    for y in range(bounds_min.y, bounds_max.y):
        line = ""
        for x in range(bounds_min.x, bounds_max.x):
            pos = Vector2(x, y)

            y_border = pos.y % grid_size.y == 0 or pos.y % grid_size.y == grid_size.y - 1
            x_border = pos.x % grid_size.x == 0 or pos.x % grid_size.x == grid_size.x - 1

            if pos in positions: line += "O"
            elif y_border and x_border: line += "+"
            elif y_border: line += "-"
            elif x_border: line += "|"
            else: 
                c = input_data.get(input_data.wrap(pos))
                if c == "#": line += "#"
                elif c == ".": line += " "
                else: line += c
        result_str += line + "\n"
    return result_str

def solve_bruteforce(input_data: InputData, target_steps_count: int, wraps: bool, show_progress: bool) -> [Vector2]:
    even_positions = set([input_data.start_pos])
    odd_positions = set()

    steps_range = range(target_steps_count)
    if show_progress: steps_range = tqdm(steps_range)
    for step in steps_range:
        cur_positions = even_positions if step % 2 == 0 else odd_positions
        next_positions = odd_positions if step % 2 == 0 else even_positions

        for cur_pos in cur_positions:
            for next_pos in get_neighbors(cur_pos):
                if not wraps and not input_data.in_bounds(next_pos): continue
                if input_data.get(input_data.wrap(next_pos)) != ".": continue
                next_positions.add(next_pos)

    final_positions = even_positions if target_steps_count % 2 == 0 else odd_positions
    return list(final_positions)

def do_part1(input_data: InputData):
    target_steps_count = 6 if IS_EXAMPLE else 64
    print(f"part1: {len(solve_bruteforce(input_data, target_steps_count, False, False))}")

def get_test_bounds(grid_size: Vector2, rep_min = Vector2(0, 0), rep_max = Vector2(1, 1)) -> (Vector2, Vector2):
    return (grid_size.scaled(rep_min), grid_size.scaled(rep_max))

def get_bounds_for_grid(grid_idx: Vector2, grid_size: Vector2):
    origin = grid_idx.scaled(grid_size)
    return (origin, origin + grid_size)

def get_bounds_edge_points(bounds: (Vector2, Vector2)) -> [Vector2]:
    bounds_min, bounds_max = bounds
    edge_points = []
    edge_points.extend([Vector2(x, bounds_min.y) for x in range(bounds_min.x, bounds_max.x)])
    edge_points.extend([Vector2(x, bounds_max.y - 1) for x in range(bounds_min.x, bounds_max.x)])
    edge_points.extend([Vector2(bounds_min.x, y) for y in range(bounds_min.y, bounds_max.y)])
    edge_points.extend([Vector2(bounds_max.x - 1, y) for y in range(bounds_min.y, bounds_max.y)])
    return edge_points

def in_bounds(point: Vector2, bounds: (Vector2, Vector2)) -> bool:
    bounds_min, bounds_max = bounds
    if point.x < bounds_min.x or point.x >= bounds_max.x: return False
    if point.y < bounds_min.y or point.y >= bounds_max.y: return False
    return True

def constrain_to_bounds(point: Vector2, bounds: (Vector2, Vector2)) -> Vector2:
    bounds_min, bounds_max = bounds
    return point.max(bounds_min).min(bounds_max - Vector2(1, 1))

def calc_min_steps_per_pos(input_data: InputData, start_pos: Vector2, bounds: (Vector2, Vector2)):
    min_steps = { start_pos: 0 }
    cur_positions = [start_pos]

    for step in range(100000000):
        next_positions = set()

        for cur_pos in cur_positions:
            for next_pos in get_neighbors(cur_pos):
                if not in_bounds(next_pos, bounds): continue
                if input_data.get(input_data.wrap(next_pos)) != ".": continue

                if next_pos in min_steps: continue

                min_steps[next_pos] = step + 1
                next_positions.add(next_pos)

        cur_positions = next_positions
        if len(cur_positions) == 0: break
    return min_steps

def test_edge_distance_assumption(input_data: InputData, max_expansion: int) -> bool:
    grid_size = input_data.grid_size
    start_pos = input_data.start_pos

    print(f"Calculating min steps for {max_expansion=}")
    min_steps_per_pos = calc_min_steps_per_pos(input_data, start_pos, get_test_bounds(grid_size, Vector2(-max_expansion, -max_expansion), Vector2(max_expansion + 1, max_expansion + 1)))

    for y_expansion in range(0, max_expansion + 1):
        for x_expansion in range(0, max_expansion + 1):
            edge_bounds = get_test_bounds(grid_size, Vector2(-x_expansion, -x_expansion), Vector2(y_expansion + 1, y_expansion + 1))
            edge_points = get_bounds_edge_points(edge_bounds)

            print(f"Expansion {x_expansion} x {y_expansion}, bounds: {edge_bounds}, edge points: {len(edge_points)}")

            for end_pos in edge_points:
                cart_distance = (end_pos - start_pos).abs().sum()
                if cart_distance != min_steps_per_pos[end_pos]:
                    print(f"MISMATCH from {start_pos} to {end_pos}, distance: {cart_distance}, steps: {min_steps_per_pos[end_pos]}")
                    return False
    return True

def find_possible_positions_for_grid(input_data: InputData, start_pos: Vector2, grid_bounds: (Vector2, Vector2), target_steps_count: int, show_progress: bool) -> (int, int):

    min_bounds, max_bounds = grid_bounds

    if start_pos.y == min_bounds.y or start_pos.y == max_bounds.y - 1: start_pos_edge_offset = Vector2(1, 0)
    elif start_pos.x == min_bounds.x or start_pos.x == max_bounds.x - 1: start_pos_edge_offset = Vector2(0, 1)
    else: start_pos_edge_offset = None

    even_positions = set([start_pos])
    odd_positions = set()

    steps_done = 0

    steps_range = range(target_steps_count)
    if show_progress: steps_range = tqdm(steps_range)
    for step in steps_range:
        cur_positions = even_positions if step % 2 == 0 else odd_positions
        next_positions = odd_positions if step % 2 == 0 else even_positions

        added_cur_pos = False
        if step > 0 and start_pos_edge_offset is not None:
            for dir in [-1, 1]:
                edge_pos = start_pos + start_pos_edge_offset * (step * dir)
                if in_bounds(edge_pos, grid_bounds):
                    cur_positions.add(edge_pos)
                    added_cur_pos = True

        prev_next_count = len(next_positions)

        for cur_pos in cur_positions:
            for next_pos in get_neighbors(cur_pos):
                if not in_bounds(next_pos, grid_bounds): continue
                if input_data.get(input_data.wrap(next_pos)) != ".": continue
                next_positions.add(next_pos)

        if not added_cur_pos and len(next_positions) == prev_next_count: 
            break # can break early

        steps_done += 1

    final_positions = even_positions if target_steps_count % 2 == 0 else odd_positions
    return steps_done, len(final_positions)

def grid_get(grid_bounds, rows, pos):
    min_bounds, max_bounds = grid_bounds
    return rows[pos.y - min_bounds.y][pos.x - min_bounds.x]

def grid_set(grid_bounds, rows, pos, value):
    min_bounds, max_bounds = grid_bounds
    rows[pos.y - min_bounds.y][pos.x - min_bounds.x] = value

def find_possible_positions_for_grid_faster(input_data: InputData, start_pos: Vector2, grid_bounds: (Vector2, Vector2), target_steps_count: int, show_progress: bool) -> (int, int):

    min_bounds, max_bounds = grid_bounds

    visited_grid = [[False] * (max_bounds.x - min_bounds.x) for _ in range(max_bounds.y - min_bounds.y)]

    cur_positions = [start_pos]
    for pos in cur_positions:
        grid_set(grid_bounds, visited_grid, pos, True)

    steps_done = 0
    even_pos_count = 0
    odd_pos_count = 0

    steps_range = range(target_steps_count + 1)
    if show_progress: steps_range = tqdm(steps_range)
    for step in steps_range:

        next_positions = []
        for cur_pos in cur_positions:
            if step % 2 == 0: even_pos_count += 1
            else: odd_pos_count += 1

            for next_pos in get_neighbors(cur_pos):
                if not in_bounds(next_pos, grid_bounds): continue
                if input_data.get(input_data.wrap(next_pos)) != ".": continue
                if grid_get(grid_bounds, visited_grid, next_pos): continue

                grid_set(grid_bounds, visited_grid, next_pos, True)
                next_positions.append(next_pos)

        if len(next_positions) == 0: 
            break # can break early

        cur_positions = next_positions
        steps_done += 1

    final_pos_count = even_pos_count if target_steps_count % 2 == 0 else odd_pos_count
    return steps_done, final_pos_count

def get_all_grid_indexes_for_bruteforce(target_steps_count: int) -> [Vector2]:
    max_expansion = 5 + target_steps_count // min(input_data.grid_size.x, input_data.grid_size.y)

    grid_indexes = []
    for grid_y in range(-max_expansion, max_expansion + 1):
        for grid_x in range(-max_expansion, max_expansion + 1):
            grid_indexes.append(Vector2(grid_x, grid_y))

    return grid_indexes

def solve_grid_based(input_data: InputData, grid_indexes: [Vector2], target_steps_count: int, show_progress: bool, print_debug: bool) -> int:
    final_positions_count = 0

    cached_grid_position_counts = {}
    cached_max_steps_to_fill = {}

    if show_progress: grid_indexes = tqdm(grid_indexes)

    for grid_idx in grid_indexes:
        grid_bounds = get_bounds_for_grid(grid_idx, input_data.grid_size)
        start_pos = constrain_to_bounds(input_data.start_pos, grid_bounds)

        start_distance = (start_pos - input_data.start_pos).abs().sum()
        remaining_steps = target_steps_count - start_distance
        if remaining_steps < 0: continue

        relative_start_pos = start_pos - grid_bounds[0]
        remaining_steps_is_odd = remaining_steps % 2 == 1
        max_steps_to_fill = cached_max_steps_to_fill.get((relative_start_pos, remaining_steps_is_odd), 100000000)

        cache_key = (relative_start_pos, remaining_steps_is_odd, min(remaining_steps, max_steps_to_fill))
        grid_positions_count = cached_grid_position_counts.get(cache_key, None)

        if print_debug:
            print(f"{grid_idx=}, {start_pos=}, {remaining_steps=}, {cache_key=}")

        if grid_positions_count is None:
            steps_done, grid_positions_count = find_possible_positions_for_grid_faster(input_data, start_pos, grid_bounds, remaining_steps, False)

            if print_debug:
                print(f"calculated: {grid_positions_count}, {remaining_steps=}, {steps_done=}")

            # cached_count = cached_grid_position_counts.get(cache_key, None)
            # print(f"Get cache: {cache_key} = {cached_count}")
            # if cached_count is not None and cached_count != grid_positions_count:
            #     print(f"CACHE ERROR: {cached_count=}")
            #     return 0

            if steps_done < remaining_steps:
                cached_max_steps_to_fill[(relative_start_pos, remaining_steps_is_odd)] = steps_done
                cache_key = (relative_start_pos, remaining_steps_is_odd, steps_done)

            cached_grid_position_counts[cache_key] = grid_positions_count
            # print(f"Set cache: {cache_key} = {grid_positions_count}")

        elif print_debug:
            print(f"from cache: {grid_positions_count}")

        final_positions_count += grid_positions_count

    return final_positions_count

def do_part2(input_data: InputData):
    target_steps_count = 100 if IS_EXAMPLE else 26501365
    grid_size = input_data.grid_size

    # print(f"Test edge distance assumption: {test_edge_distance_assumption(input_data, 3)}")

    # for bruteforce_steps in range(100, 10000000000, 100):
    #     print(f"Steps: {bruteforce_steps}, bruteforce solution: {len(solve_bruteforce(input_data, bruteforce_steps, True, True))}")
    # Steps: 300, bruteforce solution: 77106

    # test_steps = 300
    # test_bounds = get_test_bounds(grid_size, Vector2(-10, -10), Vector2(20, 20))
    # steps_done, test_positions_count = find_possible_positions_for_grid_faster(input_data, input_data.start_pos, test_bounds, test_steps, True)
    # print(f"{test_steps=}, {steps_done=} answer: {test_positions_count}")

    steps = 7000
    final_positions_count = solve_grid_based(input_data, get_all_grid_indexes_for_bruteforce(steps), steps, True, False)
    # Steps 500, answer: 214365
    # Steps 600, answer: 308952
    # Steps 700: answer: 418949
    # Steps 800, answer: 547639
    # Steps 7000, answer: (41847781?)

    print(f"part2: {final_positions_count}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
