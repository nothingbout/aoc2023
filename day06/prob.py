from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

def parse_ints(line):
    return [int(x) for x in line.split(' ') if len(x) > 0]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    times = parse_ints(lines[0][len('Time:'):])
    distances = parse_ints(lines[1][len('Distances:'):])
    return list(zip(times, distances))

start_time = datetime.now()

input_races = parse_input()

def do_part1():
    ways_to_win_array = []
    for race_time, race_distance in input_races:
        ways_to_win = 0
        for ms_held in range(0, race_time + 1):
            distance_moved = ms_held * (race_time - ms_held)
            if distance_moved > race_distance:
                ways_to_win += 1
        ways_to_win_array.append(ways_to_win)
        
    print(f"part1: {functools.reduce(lambda y, x: y * x, ways_to_win_array)}")

def do_part2():
    def combine_ints(ints):
        return int(''.join(map(str, ints)))

    race_time = combine_ints([race[0] for race in input_races])
    race_distance = combine_ints([race[1] for race in input_races])

    ways_to_win = 0
    for ms_held in range(0, race_time + 1):
        distance_moved = ms_held * (race_time - ms_held)
        if distance_moved > race_distance:
            ways_to_win += 1

    print(f"part2: {ways_to_win}")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
