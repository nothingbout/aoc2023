from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Set
from tqdm import tqdm
import operator
import functools
import itertools
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass
class InputData:
    steps: [str]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    steps = lines[0].split(",")

    return InputData(steps=steps)

def calc_hash(input: str) -> int:
    hash = 0
    for c in input:
        hash += ord(c)
        hash *= 17
        hash %= 256
    return hash

def do_part1(input_data: InputData):
    hash_sum = 0
    for step_str in input_data.steps:
        hash_sum += calc_hash(step_str)

    print(f"part1: {hash_sum}")

def parse_step(step_str: str) -> (str, str, int):
    sep_idx = max(step_str.find("="), step_str.find("-"))
    label = step_str[:sep_idx]
    op = step_str[sep_idx]
    value = int(step_str[sep_idx + 1:]) if sep_idx < len(step_str) - 1 else 0
    return (label, op, value)

def find_idx(from_list, predicate) -> int:
    for i, item in enumerate(from_list):
        if predicate(item): return i
    return -1

def do_part2(input_data: InputData):
    hash_map = [[] for _ in range(256)]
    for step_str in input_data.steps:
        label, op, value = parse_step(step_str)
        hash = calc_hash(label)

        slot_list = hash_map[hash]
        idx_in_slot = find_idx(slot_list, lambda item: item[0] == label)
        if op == "-":
            if idx_in_slot >= 0:
                slot_list.pop(idx_in_slot)
        elif op == "=":
            new_item = (label, value)
            if idx_in_slot >= 0:
                slot_list[idx_in_slot] = new_item
            else:
                slot_list.append(new_item)

    focusing_power = 0
    for slot_idx, slot_list in enumerate(hash_map):
        for item_idx, item, in enumerate(slot_list):
            focusing_power += (slot_idx + 1) * (item_idx + 1) * item[1]

    print(f"part2: {focusing_power}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
