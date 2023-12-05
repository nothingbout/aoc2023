from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = True
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

def v_set(a, idx, value):
    if idx < 0 or idx >= len(a): raise Exception(f"index out of bounds: len(a) == {len(a)}, idx == {idx}")
    return a[0:idx] + (value,) + a[idx+1 : len(a)]
def v_check(a, b):
    if isinstance(b, tuple):
        if len(a) != len(b): raise Exception(f"length mismatch: len(a) == {len(a)}, len(b) == {len(b)}")
        return True
    return False
def v_add(a, b): return tuple(map(lambda x, y: x + y, a, b)) if v_check(a, b) else tuple(map(lambda x: x + b, a))
def v_sub(a, b): return tuple(map(lambda x, y: x - y, a, b)) if v_check(a, b) else tuple(map(lambda x: x - b, a))
def v_mul(a, b): return tuple(map(lambda x, y: x * y, a, b)) if v_check(a, b) else tuple(map(lambda x: x * b, a))
def v_div(a, b): return tuple(map(lambda x, y: x / y, a, b)) if v_check(a, b) else tuple(map(lambda x: x / b, a))
def v_floor(a): return tuple(map(math.floor, a))
def v_ceil(a): return tuple(map(math.ceil, a))
def v_min(a, b): return tuple(map(lambda x, y: min(x, y), a, b)) if v_check(a, b) else None
def v_max(a, b): return tuple(map(lambda x, y: max(x, y), a, b)) if v_check(a, b) else None

def parse_until(input: str, stop_at: str) -> (str, str):
    parsed = ""
    while len(input) > 0 and not input.startswith(stop_at):
        parsed += input[0]
        input = input[1:]
    return input, parsed

def parse_int(input: str) -> (str, int):
    parsed = ""
    while len(input) > 0 and input[0].isdigit():
        parsed += input[0]
        input = input[1:]
    return input, int(parsed)


def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    return lines

start_time = datetime.now()

input_lines = parse_input()

def do_part1():
    print(input_lines)
    print(f"part1: ")

def do_part2():
    print(f"part2: ")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
