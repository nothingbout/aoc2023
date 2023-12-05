from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]
    return lines

start_time = datetime.now()

input_lines = parse_input()
grid_width = len(input_lines[0])
grid_height = len(input_lines)

next_number_id = 0
number_id_map = {}
coord_id_map = {}

def input_grid_get(coord) -> str:
    x, y = coord
    return input_lines[y][x]

def get_neighbor_coords(coord) -> (int, int):
    x, y = coord
    return [
        (x - 1, y - 1), (x - 0, y - 1), (x + 1, y - 1), 
        (x - 1, y - 0),                 (x + 1, y - 0), 
        (x - 1, y + 1), (x - 0, y + 1), (x + 1, y + 1), 
    ]

for y in range(0, grid_height):
    for x in range(0, grid_width):
        if (x, y) in coord_id_map: continue

        if input_grid_get((x, y)).isdigit(): 
            number_id = next_number_id
            next_number_id += 1
            digits = ""
            nx = x
            for nx in range(x, grid_width):
                ch = input_grid_get((nx, y))
                if not ch.isdigit(): break
                digits += ch
                coord_id_map[(nx, y)] = number_id
            number_id_map[number_id] = int(digits)

def do_part1():
    num_ids = set()
    for y in range(0, grid_height):
        for x in range(0, grid_width):
            ch = input_grid_get((x, y))
            if ch.isdigit() or ch == '.': continue

            for nc in get_neighbor_coords((x, y)):
                if nc in coord_id_map:
                    num_ids.add(coord_id_map[nc])

    print(f"part1: {sum(map(lambda id: number_id_map[id], num_ids))}")

def do_part2():
    ratios = []
    for y in range(0, grid_height):
        for x in range(0, grid_width):
            ch = input_grid_get((x, y))
            if ch != '*': continue

            num_ids = set()
            for nc in get_neighbor_coords((x, y)):
                if nc in coord_id_map:
                    num_ids.add(coord_id_map[nc])
            if len(num_ids) != 2: continue

            nums = list(map(lambda id: number_id_map[id], num_ids))
            ratios.append(nums[0] * nums[1])

    print(f"part2: {sum(ratios)}")


do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
