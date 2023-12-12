from datetime import datetime
import dataclasses;
from dataclasses import dataclass
import functools
import itertools
import time
import math
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True)
class SpringDataRow:
    cells: str
    broken_group_lengths: list

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    data_rows = []
    for line in lines:
        parts = line.split(' ')
        lengths = list(map(int, parts[1].split(',')))
        data_rows.append(SpringDataRow(cells=parts[0], broken_group_lengths=lengths))

    return data_rows

def solve_rec(data_row: SpringDataRow, cell_idx, group_idx, broken_count, results_cache):
    params_key = (cell_idx, group_idx, broken_count)
    result = results_cache.get(params_key)
    if result is not None: return result

    can_be_broken = True
    can_be_operational = True

    if group_idx == len(data_row.broken_group_lengths):
        # can't be broken, all broken springs already encountered
        can_be_broken = False
    else:
        if broken_count == data_row.broken_group_lengths[group_idx]:
            broken_count = 0
            group_idx += 1
            # can't be broken, must have at least one operational spring after a segment of broken springs
            can_be_broken = False
        elif broken_count > 0:
            # can't be operational, following a broken spring but the group is not completed
            can_be_operational = False

    if cell_idx == len(data_row.cells):
        return 1 if group_idx == len(data_row.broken_group_lengths) else 0
    
    if data_row.cells[cell_idx] == '.': can_be_broken = False
    elif data_row.cells[cell_idx] == '#': can_be_operational = False

    total_comb_count = 0

    if can_be_broken:
        total_comb_count += solve_rec(data_row, cell_idx + 1, group_idx, broken_count + 1, results_cache)

    if can_be_operational:
        total_comb_count += solve_rec(data_row, cell_idx + 1, group_idx, 0, results_cache)

    results_cache[params_key] = total_comb_count
    return total_comb_count

def solve(data_row):
    return solve_rec(data_row, 0, 0, 0, {})

def do_part1(data_rows):
    total_comb_count = 0
    for data_row in data_rows:
        comb_count = solve(data_row)
        total_comb_count += comb_count

    print(f"part1: {total_comb_count}")

def do_part2(input_data_rows):
    data_rows = []
    for input_data_row in input_data_rows:
        data_rows.append(SpringDataRow(
            cells = '?'.join([input_data_row.cells for _ in range(5)]), 
            broken_group_lengths = input_data_row.broken_group_lengths * 5
        ))

    # total_comb_count = 0
    # for data_row in tqdm(data_rows):
    #     # print(data_row)
    #     comb_count = solve(data_row)
    #     total_comb_count += comb_count

    comb_counts = process_map(solve, data_rows) #, max_workers=8)
    total_comb_count = sum(comb_counts)

    print(f"part2: {total_comb_count}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data_rows = parse_input()

    do_part1(input_data_rows)
    do_part2(input_data_rows)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
