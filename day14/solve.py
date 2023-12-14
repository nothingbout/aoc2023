from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Set
import operator
import functools
import itertools
import math
from tqdm import tqdm

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True, eq=True, frozen=True)
class Vector2:
    x: int
    y: int

    def __add__(a, b):
        return Vector2(a.x + b.x, a.y + b.y)

    def __sub__(a, b):
        return Vector2(a.x - b.x, a.y - b.y)

@dataclass
class InputData:
    grid_size: Vector2
    cube_rocks: Set[Vector2]
    round_rocks: Set[Vector2]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grid_size = Vector2(len(lines[0]), len(lines))
    cube_rocks = []
    round_rocks = []
    for y in range(grid_size.y):
        for x in range(grid_size.x):
            pos = Vector2(x, y)
            match lines[y][x]:
                case '#': cube_rocks.append(pos)
                case 'O': round_rocks.append(pos)

    return InputData(grid_size, cube_rocks=set(cube_rocks), round_rocks=set(round_rocks))

def pretty_print(grid_size: Vector2, cube_rocks, round_rocks):
    for y in range(grid_size.y):
        line = ""
        for x in range(grid_size.x):
            if Vector2(x, y) in round_rocks: line += "O"
            elif Vector2(x, y) in cube_rocks: line += "#"
            else: line += "."
        print(line)
    print()

def tilt(grid_size: Vector2, cube_rocks: Set[Vector2], round_rocks: Set[Vector2]) -> Set[Vector2]:
    new_round_rocks = set()
    for x in range(grid_size.x):
        start_y = 0
        while start_y < grid_size.y:
            end_y = grid_size.y
            num_round_rocks = 0
            for y in range(start_y, grid_size.y):
                if Vector2(x, y) in cube_rocks:
                    end_y = y
                    break
                elif Vector2(x, y) in round_rocks:
                    num_round_rocks += 1

            for y in range(start_y, start_y + num_round_rocks):
                new_round_rocks.add(Vector2(x, y))

            start_y = end_y + 1

    return new_round_rocks

def calc_load(round_rocks, grid_size):
    return sum(map(lambda p: grid_size.y - p.y, round_rocks))

def do_part1(input_data: InputData):
    tilted_rocks = tilt(input_data.grid_size, input_data.cube_rocks, input_data.round_rocks)

    load = calc_load(tilted_rocks, input_data.grid_size)

    print(f"part1: {load}")

def rotated_pos(pos: Vector2, grid_size) -> Vector2:
    return Vector2(grid_size.y - 1 - pos.y, pos.x)

def rotated_pos_set(pos_set: Set[Vector2], grid_size: Vector2) -> Set[Vector2]:
    return set(map(lambda pos: rotated_pos(pos, grid_size), pos_set))

def do_part2(input_data: InputData):

    cube_rocks_by_rotation = [input_data.cube_rocks]
    for _ in range(3):
        cube_rocks_by_rotation.append(rotated_pos_set(cube_rocks_by_rotation[-1], input_data.grid_size))

    tilted_rocks = input_data.round_rocks

    loads = []
    prev_load_indexes = {}
    repeating_cycle_interval = None

    max_cycle = 1000000000
    cycle = 0
    while cycle < max_cycle:
        for rot in range(4):
            tilted_rocks = tilt(input_data.grid_size, cube_rocks_by_rotation[rot], tilted_rocks)
            tilted_rocks = rotated_pos_set(tilted_rocks, input_data.grid_size)
            loads.append(calc_load(tilted_rocks, input_data.grid_size))

        if repeating_cycle_interval is None:
            load_idx = len(loads) - 1
            load = loads[load_idx]
            if prev_idx := prev_load_indexes.get(load):
                if prev_idx > load_idx - prev_idx:
                    mismatch = False
                    for i in range(load_idx - prev_idx):
                        if loads[load_idx - i] != loads[prev_idx - i]:
                            mismatch = True
                            break
                    if not mismatch:
                        repeating_cycle_interval = load_idx - prev_idx

            prev_load_indexes[load] = load_idx

            if repeating_cycle_interval is not None:
                new_cycle = cycle + int((max_cycle - 1 - cycle) / repeating_cycle_interval) * repeating_cycle_interval
                print(f"Repeating cycle found at {cycle} with interval {repeating_cycle_interval}, skipping to cycle {new_cycle}")
                cycle = new_cycle

        cycle += 1
        # print(f"After {cycle} cycles:")
        # pretty_print(input_data.grid_size, input_data.cube_rocks, tilted_rocks)

    load = calc_load(tilted_rocks, input_data.grid_size)

    print(f"part2: {load}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
