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
    grid_size: Vector2
    rows: [str]

    def get(self, pos: Vector2) -> str:
        return self.rows[pos.y][pos.x]
    
    def in_bounds(self, pos: Vector2) -> bool:
        if pos.x < 0 or pos.x >= self.grid_size.x: return False
        if pos.y < 0 or pos.y >= self.grid_size.y: return False
        return True

@dataclass(slots=True, eq=True, frozen=True)
class BeamState:
    pos: Vector2
    dir: Vector2

    def next_beam(self, dir: Vector2):
        return BeamState(self.pos + dir, dir)

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grid_size = Vector2(len(lines[0]), len(lines))

    return InputData(grid_size=grid_size, rows=lines)

def get_beams_by_pos(beams: Set[BeamState]) -> Dict[Vector2, List[Vector2]]:
    beams_by_pos = {}
    for beam in beams:
        if not beam.pos in beams_by_pos:
            beams_by_pos[beam.pos] = []
        beams_by_pos[beam.pos].append(beam.dir)
    return beams_by_pos

def pretty_print(input_data: InputData, beams_set=set()):
    beams_by_pos = get_beams_by_pos(beams_set)

    for y in range(input_data.grid_size.y):
        line = ""
        for x in range(input_data.grid_size.x):
            cell = input_data.get(Vector2(x, y))
            if cell == '.':
                if beams := beams_by_pos.get(Vector2(x, y)):
                    if len(beams) > 1:
                        cell = str(int(len(beams)))
                    else:
                        match beams[0]:
                            case Vector2(0, -1): cell = '^'
                            case Vector2(-1, 0): cell = '<'
                            case Vector2(0, 1): cell = 'v'
                            case Vector2(1, 0): cell = '>'
            line += cell
        print(line)
    print()

def solve_rec(input_data: InputData, seen_beams: Set[BeamState], cur_beam: BeamState):
    if not input_data.in_bounds(cur_beam.pos): return

    if cur_beam in seen_beams: return
    seen_beams.add(cur_beam)

    split = False
    reflect_dir = None
    match input_data.get(cur_beam.pos):
        case '|': 
            if cur_beam.dir.x != 0: split = True
        case '-': 
            if cur_beam.dir.y != 0: split = True
        case '/':
            if cur_beam.dir.x != 0: reflect_dir = Vector2(0, -cur_beam.dir.x)
            else: reflect_dir = Vector2(-cur_beam.dir.y, 0)
        case '\\':
            if cur_beam.dir.x != 0: reflect_dir = Vector2(0, cur_beam.dir.x)
            else: reflect_dir = Vector2(cur_beam.dir.y, 0)

    if split:
        solve_rec(input_data, seen_beams, cur_beam.next_beam(cur_beam.dir.rotated_ccw()))
        solve_rec(input_data, seen_beams, cur_beam.next_beam(-cur_beam.dir.rotated_ccw()))
    elif reflect_dir is not None:
        solve_rec(input_data, seen_beams, cur_beam.next_beam(reflect_dir))
    else:
        solve_rec(input_data, seen_beams, cur_beam.next_beam(cur_beam.dir))

def solve(input_data, start_beam) -> int:
    seen_beams = set()
    solve_rec(input_data, seen_beams, start_beam)
    # pretty_print(input_data, seen_beams)
    return len(list(get_beams_by_pos(seen_beams).keys()))

def do_part1(input_data: InputData):
    energized = solve(input_data, BeamState(Vector2(0, 0), Vector2(1, 0)))
    print(f"part1: {energized}")

def do_part2(input_data: InputData):
    start_beams = []
    for x in range(input_data.grid_size.x):
        start_beams.append(BeamState(Vector2(x, 0), Vector2(0, 1)))
        start_beams.append(BeamState(Vector2(x, input_data.grid_size.y - 1), Vector2(0, -1)))

    for y in range(input_data.grid_size.y):
        start_beams.append(BeamState(Vector2(0, y), Vector2(1, 0)))
        start_beams.append(BeamState(Vector2(input_data.grid_size.x - 1, y), Vector2(-1, 0)))

    most_energized = 0
    for start_beam in tqdm(start_beams):
        most_energized = max(most_energized, solve(input_data, start_beam))

    print(f"part2: {most_energized}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
