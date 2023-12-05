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

    seeds = [int(x) for x in lines[0][7:].split(' ')]
    lines = lines[2:]

    maps = {}
    while len(lines) > 0:
        src_type, _, dst_type = lines[0].split(' ')[0].split('-')
        print(f"{src_type} -> {dst_type}")
        lines = lines[1:]
        ranges = []
        while len(lines) > 0 and len(lines[0]) > 0:
            dst_start, src_start, count = [int(x) for x in lines[0].split(' ')]
            lines = lines[1:]
            ranges.append((dst_start, src_start, count))
        lines = lines[1:]
        maps[src_type] = {
            'dst_type': dst_type, 
            'ranges': ranges
        }

    return seeds, maps

start_time = datetime.now()

input_seeds, input_maps = parse_input()

def do_part1():
    cur_type = 'seed'
    cur_numbers = list(input_seeds)
    while True:
        cur_map = input_maps.get(cur_type)
        if cur_map is None: break

        map_ranges = cur_map['ranges']

        new_numbers = []
        for num in cur_numbers:
            for dst_start, src_start, range_len in map_ranges:
                if num >= src_start and num < src_start + range_len:
                    num = dst_start + (num - src_start)
                    break
            new_numbers.append(num)

        cur_type = cur_map['dst_type']
        cur_numbers = new_numbers
    
    print(f"part1: {min(cur_numbers)}")

def do_part2():
    input_ranges = []
    for i in range(0, len(input_seeds), 2):
        input_ranges.append((input_seeds[i + 0], input_seeds[i + 1]))

    cur_type = 'seed'
    cur_ranges = list(input_ranges)

    while True:
        cur_map = input_maps.get(cur_type)
        if cur_map is None: break
        map_ranges = cur_map['ranges']

        unmapped_ranges = list(cur_ranges)
        mapped_ranges = []
        for map_dst, map_src, map_len in map_ranges:
            new_unmapped_ranges = []

            for start, count in unmapped_ranges:
                if start < map_src:
                    new_unmapped_ranges.append((start, min(count, map_src - start)))

                if start + count > map_src + map_len:
                    new_start = max(start, map_src + map_len)
                    new_unmapped_ranges.append((new_start, start + count - new_start))

                intersect_start = max(start, map_src)
                intersect_len = min(start + count, map_src + map_len) - intersect_start
                if intersect_len > 0:
                    mapped_ranges.append((intersect_start + (map_dst - map_src), intersect_len))
           
            unmapped_ranges = new_unmapped_ranges

        cur_ranges = unmapped_ranges + mapped_ranges
        cur_type = cur_map['dst_type']

    print(f"part2: {min([r[0] for r in cur_ranges])}")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
