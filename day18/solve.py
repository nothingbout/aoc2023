from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set
from tqdm import tqdm
import operator
import functools
import itertools
import math
import sys

sys.setrecursionlimit(100000)

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
    def min(a, b): return Vector2(min(a.x, b.x), min(a.y, b.y))
    def max(a, b): return Vector2(max(a.x, b.x), max(a.y, b.y))

@dataclass(slots=True, frozen=True)
class Instruction:
    dir: Vector2
    steps: int
    color: str

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    instructions = []

    for line in lines:
        cols = line.split(' ')
        match cols[0]:
            case 'U': dir = Vector2(0, -1)
            case 'L': dir = Vector2(-1, 0)
            case 'D': dir = Vector2(0, 1)
            case 'R': dir = Vector2(1, 0)
        steps = int(cols[1])
        color = cols[2][2:-1]
        instructions.append(Instruction(dir, steps, color))

    return instructions

def pretty_print(digged_positions = Set[Vector2]):
    bounds_min = functools.reduce(Vector2.min, digged_positions, next(iter(digged_positions)))
    bounds_max = functools.reduce(Vector2.max, digged_positions, next(iter(digged_positions)))

    for y in range(bounds_min.y, bounds_max.y + 1):
        line = ""
        for x in range(bounds_min.x, bounds_max.x + 1):
            pos = Vector2(x, y)
            if pos in digged_positions: line += "#"
            else: line += " "
        print(line)

def do_part1(input_data: [Instruction]):
    start_pos = Vector2(0, 0)
    digged_positions = []

    cur_pos = start_pos
    for instruction in input_data:
        for _ in range(instruction.steps):
            cur_pos += instruction.dir
            digged_positions.append(cur_pos)
    
    def floodfill(p, p_set):
        if p in p_set: return
        p_set.add(p)
        for dir in [Vector2(*x) for x in [(-1, 0), (0, -1), (1, 0), (0, 1)]]:
            floodfill(p + dir, p_set)

    digged_pos_set = set(digged_positions)
    # pretty_print(digged_pos_set)

    for i in range(len(digged_positions)):
        a = digged_positions[i]
        b = digged_positions[(i + 1) % len(digged_positions)]
        n_dir = -(b - a).rotated_ccw()
        floodfill(a + n_dir, digged_pos_set)
        floodfill(b + n_dir, digged_pos_set)

    print(f"part1: {len(digged_pos_set)}")

def decode_color_instruction(instruction: Instruction) -> Instruction:
    steps = int(instruction.color[:5], 16)
    match instruction.color[5]:
        case '0': dir = Vector2(1, 0)
        case '1': dir = Vector2(0, 1)
        case '2': dir = Vector2(-1, 0)
        case '3': dir = Vector2(0, -1)
    return Instruction(dir, steps, "")

def do_part2(input_data: [Instruction]):
    instructions = list(map(decode_color_instruction, input_data))

    points = []
    cur_pos = Vector2(0, 0)
    for instruction in instructions:
        cur_pos += instruction.dir * instruction.steps
        points.append(cur_pos)

    total_area = 0
    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]
        total_area += (a.x * b.y - b.x * a.y)
    
    total_area //= 2

    # account for under-counted right and bottom perimeters
    perimeter = sum([i.steps for i in instructions])
    total_area += perimeter // 2 + 1

    print(f"part2: {total_area}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
