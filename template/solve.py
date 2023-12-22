from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math

# import heapq
#
# search_visited = set()
# search_queue = [(0, start_state)]
# heapq.heapify(search_queue)
#
# while len(search_queue) > 0:
#     (cur_cost, cur_state) = heapq.heappop(search_queue)
#     if cur_state in search_visited: continue
#     search_visited.add(cur_state)
#
#     for next_state in next_states:
#         heapq.heappush(search_queue, (next_cost, next_state))

IS_EXAMPLE = True
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

@dataclass
class InputData:
    lines: [str]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    return InputData(lines=lines)

def do_part1(input_data: InputData):
    print(input_data.lines)
    print(f"part1: ")

def do_part2(input_data: InputData):
    print(f"part2: ")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
