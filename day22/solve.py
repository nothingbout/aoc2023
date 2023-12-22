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
class Vector3:
    x: int
    y: int
    z: int
    def __neg__(a): return Vector3(-a.x, -a.y, -a.z)
    def __add__(a, b): return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)
    def __sub__(a, b): return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)
    def __mul__(a, s): return Vector3(a.x * s, a.y * s, a.z * s)
    def abs(a): return Vector3(abs(a.x), abs(a.y), abs(a.z))
    def sum(a): return a.x + a.y + a.z
    def scaled(a, b): return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)
    def min(a, b): return Vector3(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z))
    def max(a, b): return Vector3(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))

    def __str__(a): return f"({a.x}, {a.y}, {a.z})"
    def __repr__(a): return str(a)

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Brick:
    idx: int
    p1: Vector3
    p2: Vector3

    def get_bounds(self) -> (Vector3, Vector3):
        return (Vector3.min(self.p1, self.p2), Vector3.max(self.p1, self.p2))
    
    def offset(self, amount: Vector3) -> Self:
        return Brick(self.idx, self.p1 + amount, self.p2 + amount)

@dataclass
class InputData:
    bricks: [Brick]

def parse_vector3(input: str) -> Vector3:
    parts = input.split(',')
    return Vector3(int(parts[0]), int(parts[1]), int(parts[2]))

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    bricks = []
    for i, line in enumerate(lines):
        parts = line.split("~")
        bricks.append(Brick(i, parse_vector3(parts[0]), parse_vector3(parts[1])))

    return InputData(bricks=bricks)

def solve_supports(input_data: InputData):
    bricks_by_height = sorted(input_data.bricks, key=lambda b: min(b.p1.z, b.p2.z))
    # print('\n'.join(map(str, bricks_by_height)))

    fallen_bricks = []
    highest_fallen_grid = {}
    supports = {b.idx: [] for b in bricks_by_height}
    supported_by = {b.idx: [] for b in bricks_by_height}

    for brick in bricks_by_height:
        b_min, b_max = brick.get_bounds()
        highest_z_under = 0
        highest_idxs = []
        for y in range(b_min.y, b_max.y + 1):
            for x in range(b_min.x, b_max.x + 1):
                i, z = highest_fallen_grid.get((x, y), (-1, -1))
                if z > highest_z_under:
                    highest_z_under = z
                    highest_idxs.clear()
                    highest_idxs.append(i)
                elif z == highest_z_under and i not in highest_idxs:
                    highest_idxs.append(i)

        supported_by[brick.idx].extend(highest_idxs)
        for i in highest_idxs:
            supports[i].append(brick.idx)

        fall_amount = highest_z_under + 1 - b_min.z
        assert(fall_amount <= 0)

        fallen = brick.offset(Vector3(0, 0, fall_amount))
        fallen_bricks.append(fallen)

        # print(f"{brick.idx} falls {drop_amount}")

        for y in range(b_min.y, b_max.y + 1):
            for x in range(b_min.x, b_max.x + 1):
                highest_fallen_grid[(x, y)] = (brick.idx, b_max.z + fall_amount)

    return supports, supported_by

def do_part1(input_data: InputData):
    bricks_by_idx = input_data.bricks
    supports, supported_by = solve_supports(input_data)

    safe_to_remove_count = 0
    for brick in bricks_by_idx:
        is_critical_support = False
        for supported_idx in supports[brick.idx]:
            supported_brick = bricks_by_idx[supported_idx]
            if len(supported_by[supported_brick.idx]) == 1: 
                is_critical_support = True
                break

        if not is_critical_support:
            safe_to_remove_count += 1

    print(f"part1: {safe_to_remove_count}")

def do_part2(input_data: InputData):
    supports, supported_by = solve_supports(input_data)

    total_fall_count = 0

    for root_brick in input_data.bricks:
        falling_bricks = set([root_brick.idx])
        bricks_to_process = [root_brick.idx]

        while len(bricks_to_process) > 0:
            brick_idx = bricks_to_process.pop(0)

            for supported_idx in supports[brick_idx]:
                if supported_idx in falling_bricks: continue

                for supported_by_idx in supported_by[supported_idx]:
                    if supported_by_idx not in falling_bricks:
                        break
                else:
                    bricks_to_process.append(supported_idx)
                    falling_bricks.add(supported_idx)

        # print(f"destroying {root_brick.idx} causes {len(falling_bricks) - 1} bricks to fall")
        total_fall_count += len(falling_bricks) - 1

    print(f"part2: {total_fall_count}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
