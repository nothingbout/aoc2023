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

    cards = []
    for line in lines:
        set_inputs = line.split(':')[1].split('|')
        sets = []
        for set_input in set_inputs:
            nums = [int(c.strip()) for c in set_input.split(' ') if len(c) > 0]
            sets.append(nums)
        cards.append(sets)

    return cards

start_time = datetime.now()

input_cards = parse_input()

def get_winning_number_count(card):
    winning_nums = set(card[0])
    my_nums = card[1]
    count = 0
    for num in my_nums:
        if num in winning_nums:
            count += 1
    return count

def do_part1():
    scores = []
    for card in input_cards:
        winning_count = get_winning_number_count(card)
        score = pow(2, winning_count - 1) if winning_count > 0 else 0
        scores.append(score)

    print(f"part1: {sum(scores)}")

def do_part2():
    how_many_per = [1 for _ in range(0, len(input_cards))]
    for idx in range(0, len(input_cards)):
        winning_count = get_winning_number_count(input_cards[idx])
        how_many = how_many_per[idx]
        for i in range(idx + 1, min(len(input_cards), idx + 1 + winning_count)):
            how_many_per[i] += how_many
       
    print(f"part2: {sum(how_many_per)}")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
