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

def do_part1():
    total = 0
    for line in input_lines:
        first = next(c for c in line if c.isdigit())
        last = next(c for c in reversed(line) if c.isdigit())
        num = int(first + last)
        total += num
    print(total)

def do_part2():
    digit_name_map = {
        "one": "1", 
        "two": "2", 
        "three": "3", 
        "four": "4", 
        "five": "5", 
        "six": "6", 
        "seven": "7", 
        "eight": "8", 
        "nine": "9", 
    }

    def get_digit(text: str) -> str:
        if text[0].isdigit(): return text[0]
        for name, digit in digit_name_map.items():
            if text.startswith(name): return digit
        return None

    total = 0
    for line in input_lines:
        for i in range(0, len(line)):
            first = get_digit(line[i:])
            if first is not None: break

        for i in range(len(line) - 1, -1, -1):
            last = get_digit(line[i:])
            if last is not None: break

        num = int(first + last)
        total += num

    print(total)    

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
