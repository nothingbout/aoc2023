from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = "example3.txt" if IS_EXAMPLE else "input.txt"

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    instructions = lines[0]

    map = {}
    for line in lines[2:]:
        cols = line.split(' = ')
        src = cols[0]
        dst = cols[1][1:-1].split(', ')
        map[src] = dst

    return instructions, map

start_time = datetime.now()

def do_part1():
    input_instructions, input_map = parse_input()

    instruction_idx = 0
    current_node = 'AAA'
    total_steps = 0
    while True:
        instruction = input_instructions[instruction_idx]

        current_branch = input_map[current_node]
        next_node = current_branch[0] if instruction == 'L' else current_branch[1]

        total_steps += 1

        instruction_idx += 1
        if instruction_idx >= len(input_instructions): instruction_idx = 0

        current_node = next_node
        if current_node == 'ZZZ':
            break

    print(f"part1: {total_steps}")

def do_part2():
    input_instructions, input_map = parse_input()

    instruction_idx = 0
    current_nodes = [n for n in input_map.keys() if n.endswith('A')]
    nodes_finished_at = [0 for _ in range(0, len(current_nodes))]

    total_steps = 0
    while True:
        instruction = input_instructions[instruction_idx]

        for i in range(0, len(current_nodes)):
            if nodes_finished_at[i] > 0: continue
            current_node = current_nodes[i]

            if current_node.endswith('Z'):
                nodes_finished_at[i] = total_steps
            else:
                current_branch = input_map[current_node]
                next_node = current_branch[0] if instruction == 'L' else current_branch[1]
                current_nodes[i] = next_node

        total_steps += 1
        instruction_idx = (instruction_idx + 1) % len(input_instructions)

        if not 0 in nodes_finished_at: break

    def calc_gcd(a, b):
        greatest = 0
        for n in range(2, min(a, b) + 1):
            if a % n == 0 and b % n == 0:
                greatest = n
        return greatest
    
    def calc_lcm(a, b):
        gcd = calc_gcd(a, b)
        return int(a * b / gcd)

    total_lcm = nodes_finished_at[0]
    for n in nodes_finished_at[1:]:
        total_lcm = calc_lcm(total_lcm, n)

    print(f"part2: {total_lcm}")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
