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

    histories = []
    for line in lines:
        histories.append([int(x) for x in line.split()])

    return histories

def calculate_deltas(values):
    all_deltas = [values]
    while True:
        prev_values = all_deltas[-1]
        deltas = [0 for _ in range(0, len(prev_values) - 1)]
        has_non_zero = False
        for i in range(0, len(deltas)):
            deltas[i] = prev_values[i + 1] - prev_values[i]
            if deltas[i] != 0:
                has_non_zero = True
        all_deltas.append(deltas)
        if not has_non_zero:
            break
    return all_deltas

def do_part1(input_histories):
    all_extrapolated_values = []
    for values in input_histories:
        all_deltas = calculate_deltas(values)

        extrapolated_value = 0
        for deltas in reversed(all_deltas):
            extrapolated_value = deltas[-1] + extrapolated_value
        all_extrapolated_values.append(extrapolated_value)

    print(f"part1: {sum(all_extrapolated_values)}")

def do_part2(input_histories):
    all_extrapolated_values = []
    for values in input_histories:
        all_deltas = calculate_deltas(values)

        extrapolated_value = 0
        for deltas in reversed(all_deltas):
            extrapolated_value = deltas[0] - extrapolated_value
        all_extrapolated_values.append(extrapolated_value)

    print(f"part2: {sum(all_extrapolated_values)}")

start_time = datetime.now()
input_histories = parse_input()

do_part1(input_histories)
do_part2(input_histories)

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
