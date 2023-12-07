from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

def card_value(c):
    match c:
        case 'A': return 14
        case 'K': return 13
        case 'Q': return 12
        case 'J': return 11
        case 'T': return 10
    return int(c)

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    hands_and_bids = []
    for line in lines:
        cols = line.split(' ')
        cards = [card_value(c) for c in cols[0]]
        bid = int(cols[1])
        hands_and_bids.append((cards, bid))

    return hands_and_bids

start_time = datetime.now()

input_hands_and_bids = parse_input()

def count_cards(cards):
    counts = [0 for _ in range(0, 15)]
    for c in cards:
        counts[c] += 1
    return counts

def hand_type(cards):
    counts = count_cards(cards)
    sorted_counts = sorted(counts[2:], reverse=True)
    jokers_count = counts[1]
    
    if sorted_counts[0] + jokers_count == 5: hand_type = 7
    elif sorted_counts[0] + jokers_count == 4: hand_type = 6
    elif sorted_counts[0] + jokers_count == 3 and sorted_counts[1] == 2: hand_type = 5
    elif sorted_counts[0] + jokers_count == 3: hand_type = 4
    elif sorted_counts[0] == 2 and sorted_counts[1] == 2: hand_type = 3
    elif sorted_counts[0] + jokers_count == 2: hand_type = 2
    else: hand_type = 1

    return hand_type

def hand_high_card_value(cards):
    value = 0
    for c in cards:
        value *= 16
        value += c
    return value

def calculate_winnings(hands_and_bids):
    max_hand_high_card_value = hand_high_card_value([14 for _ in range(0, 5)])
    
    input_hand_values_bids = []
    for cards, bid in hands_and_bids:
        hand_value = hand_type(cards) * max_hand_high_card_value + hand_high_card_value(cards)
        input_hand_values_bids.append((hand_value, bid))
        

    input_hand_values_bids.sort()

    total_winnings = 0
    for rank, value_bid in enumerate(input_hand_values_bids):
        _, bid = value_bid
        total_winnings += (rank + 1) * bid
    return total_winnings

def do_part1():
    total_winnings = calculate_winnings(input_hands_and_bids)
    print(f"part1: {total_winnings}")

def do_part2():
    new_input_hands_and_bids = []
    for cards, bid in input_hands_and_bids:
        new_cards = [c if c != 11 else 1 for c in cards]
        new_input_hands_and_bids.append((new_cards, bid))

    total_winnings = calculate_winnings(new_input_hands_and_bids)
    print(f"part2: {total_winnings}")

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
