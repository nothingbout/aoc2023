from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set
from tqdm import tqdm
import operator
import functools
import itertools
import math

IS_EXAMPLE = True
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True, eq=True, frozen=True)
class Vector2:
    x: int
    y: int
    def __neg__(a): return Vector2(-a.x, -a.y)
    def __add__(a, b): return Vector2(a.x + b.x, a.y + b.y)
    def __sub__(a, b): return Vector2(a.x - b.x, a.y - b.y)
    def rotated_ccw(a): return Vector2(a.y, -a.x)

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
