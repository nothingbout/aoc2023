from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set
from tqdm import tqdm
import operator
import functools
import itertools
import math
import heapq

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

USE_HEURISTICS = False

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Vector2:
    x: int
    y: int
    def __neg__(a): return Vector2(-a.x, -a.y)
    def __add__(a, b): return Vector2(a.x + b.x, a.y + b.y)
    def __sub__(a, b): return Vector2(a.x - b.x, a.y - b.y)
    def rotated_ccw(a): return Vector2(a.y, -a.x)

@dataclass
class InputData:
    grid_size: Vector2
    heat_loss_grid: [[int]]

    def get_heat_loss(self, pos: Vector2) -> int:
        return self.heat_loss_grid[pos.y][pos.x]
    
    def in_bounds(self, pos: Vector2) -> bool:
        if pos.x < 0 or pos.x >= self.grid_size.x: return False
        if pos.y < 0 or pos.y >= self.grid_size.y: return False
        return True


@dataclass(slots=True, frozen=True, eq=True, order=True)
class SearchState:
    pos: Vector2
    dir: Vector2
    straight_moves: int

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grid_size = Vector2(len(lines[0]), len(lines))
    heat_loss_grid = []
    for line in lines:
        heat_loss_grid.append([int(c) for c in line])

    return InputData(grid_size, heat_loss_grid=heat_loss_grid)

# heuristic function for a-star, minimum heat loss when ignoring straight move requirements
def search_min_heat_loss_per_pos(input_data: InputData) -> Dict[Vector2, int]:
    search_start_pos = Vector2(0, 0)

    min_heat_loss_per_pos = {}
    search_queue = [(0, search_start_pos)]
    heapq.heapify(search_queue)

    while len(search_queue) > 0:
        (cur_heat_loss, cur_pos) = heapq.heappop(search_queue)
        if cur_pos in min_heat_loss_per_pos: continue
        min_heat_loss_per_pos[cur_pos] = cur_heat_loss

        if len(min_heat_loss_per_pos.keys()) == input_data.grid_size.x * input_data.grid_size.y:
            break

        possible_dirs = [Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1), Vector2(1, 0)]
        for dir in possible_dirs:
            next_pos = cur_pos + dir
            if not input_data.in_bounds(next_pos): continue
            next_heat_loss = cur_heat_loss + input_data.get_heat_loss(next_pos)
            heapq.heappush(search_queue, (next_heat_loss, next_pos))

    return min_heat_loss_per_pos


def search_best_path(input_data: InputData, min_straight_moves: int, max_straight_moves: int) -> int:
    search_start_pos = Vector2(0, 0)
    search_end_pos = input_data.grid_size - Vector2(1, 1)

    if USE_HEURISTICS:
        min_heat_loss_per_pos = search_min_heat_loss_per_pos(input_data)

    search_visited = set()
    if USE_HEURISTICS:
        search_queue = [(0, (0, SearchState(pos=search_start_pos, dir=Vector2(1, 0), straight_moves=0)))]
    else:
        search_queue = [(0, SearchState(pos=search_start_pos, dir=Vector2(1, 0), straight_moves=0))]

    heapq.heapify(search_queue)

    min_total_heat_loss = None
    with tqdm(total=input_data.grid_size.x * input_data.grid_size.y * 4 * max_straight_moves) as progress_bar:

        while len(search_queue) > 0:
            if USE_HEURISTICS:
                (_, (cur_heat_loss, cur_state)) = heapq.heappop(search_queue)
            else:
                (cur_heat_loss, cur_state) = heapq.heappop(search_queue)

            if cur_state in search_visited: continue
            search_visited.add(cur_state)
            progress_bar.update(1)

            if cur_state.pos == search_end_pos and cur_state.straight_moves >= min_straight_moves:
                min_total_heat_loss = cur_heat_loss
                break

            possible_dirs = []

            if cur_state.straight_moves == 0 or cur_state.straight_moves >= min_straight_moves:
                possible_dirs.append(cur_state.dir.rotated_ccw())
                possible_dirs.append(-cur_state.dir.rotated_ccw())

            if cur_state.straight_moves == 0 or cur_state.straight_moves < max_straight_moves:
                possible_dirs.append(cur_state.dir)

            for next_dir in possible_dirs:
                next_pos = cur_state.pos + next_dir
                if not input_data.in_bounds(next_pos): continue

                next_heat_loss = cur_heat_loss + input_data.get_heat_loss(next_pos)
                next_moved_straight = cur_state.straight_moves + 1 if next_dir == cur_state.dir else 1

                next_state = SearchState(next_pos, next_dir, next_moved_straight)

                if USE_HEURISTICS:
                    heuristics_value = min_heat_loss_per_pos[search_end_pos] - min_heat_loss_per_pos[next_pos]                    
                    next_heat_loss_estimate = next_heat_loss + heuristics_value
                    heapq.heappush(search_queue, (next_heat_loss_estimate, (next_heat_loss, next_state)))
                else:
                    heapq.heappush(search_queue, (next_heat_loss, next_state))

    return min_total_heat_loss
    

def do_part1(input_data: InputData):
    min_total_heat_loss = search_best_path(input_data, 1, 3)
    print(f"part1: {min_total_heat_loss}")

def do_part2(input_data: InputData):
    min_total_heat_loss = search_best_path(input_data, 4, 10)
    print(f"part2: {min_total_heat_loss}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
