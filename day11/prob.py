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

    galaxies = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((x, y))
    return galaxies

def calc_expanded_1d_distance(all_positions, start_pos, end_pos, expansion_multiplier):
    if end_pos < start_pos:
        tmp = end_pos
        end_pos = start_pos
        start_pos = tmp

    start_idx = all_positions.index(start_pos)
    cur_pos = start_pos
    expanded_distance = 0
    for i in range(start_idx + 1, len(all_positions)):
        next_pos = all_positions[i]
        if next_pos > end_pos: break
        expanded_distance += 1 + (next_pos - cur_pos - 1) * expansion_multiplier
        cur_pos = next_pos
    return expanded_distance

def calc_total_expanded_distance(input_galaxies, expansion_multiplier):
    galaxy_xs = sorted(list(set([g[0] for g in input_galaxies])))
    galaxy_ys = sorted(list(set([g[1] for g in input_galaxies])))

    total_expanded_distance = 0
    for i1 in range(0, len(input_galaxies)):
        for i2 in range(i1 + 1, len(input_galaxies)):
            p1 = input_galaxies[i1]
            p2 = input_galaxies[i2]
            expanded_x = calc_expanded_1d_distance(galaxy_xs, p1[0], p2[0], expansion_multiplier)
            expanded_y = calc_expanded_1d_distance(galaxy_ys, p1[1], p2[1], expansion_multiplier)
            total_expanded_distance += expanded_x + expanded_y

    return total_expanded_distance

def do_part1(input_galaxies):
    total_expanded_distance = calc_total_expanded_distance(input_galaxies, 2)
    print(f"part1: {total_expanded_distance}")

def do_part2(lines):
    total_expanded_distance = calc_total_expanded_distance(input_galaxies, 1000000)
    print(f"part2: {total_expanded_distance}")

start_time = datetime.now()
input_galaxies = parse_input()

do_part1(input_galaxies)
do_part2(input_galaxies)

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
