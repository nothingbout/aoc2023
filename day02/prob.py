from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

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

    games = []

    for line in lines:
        line, _ = parse_until(line, " ")
        line = line[1:]
        line, game_id = parse_int(line)
        line = line[2:]
        sets = []
        for set_input in line.split("; "):
            cube_inputs = set_input.split(", ")
            cube_counts = {}
            for cube_input in cube_inputs:
                cube_input, cube_count = parse_int(cube_input)
                cube_color = cube_input[1:]
                # print(f"{cube_color}: {cube_count}")
                cube_counts[cube_color] = cube_count
            sets.append(cube_counts)
        games.append({
            "id": game_id, 
            "sets": sets
        })

    return games

start_time = datetime.now()

input_games = parse_input()
# print(input_games)

def do_part1():
    max_counts = {
        "red": 12, 
        "green": 13, 
        "blue": 14
    }

    possible_games = []
    for game in input_games:
        possible = True
        for set in game["sets"]:
            for color, count in set.items():
                if count > max_counts[color]:
                    possible = False
        if possible:
            possible_games.append(game)

    print(sum(map(lambda game: game["id"], possible_games)))

def do_part2():
    powers = []
    for game in input_games:
        min_counts = {
            "red": 0, 
            "green": 0, 
            "blue": 0
        }

        for set in game["sets"]:
            for color, count in set.items():
                if count > min_counts[color]:
                    min_counts[color] = count
        powers.append(math.prod(min_counts.values()))

    print(sum(powers))

do_part1()
do_part2()

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
