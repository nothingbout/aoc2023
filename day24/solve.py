from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Vector3:
    x: float
    y: float
    z: float
    def __neg__(a): return Vector3(-a.x, -a.y, -a.z)
    def __add__(a, b): return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)
    def __sub__(a, b): return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)
    def __mul__(a, s): return Vector3(a.x * s, a.y * s, a.z * s)
    def __truediv__(a, s): return Vector3(a.x / s, a.y / s, a.z / s)
    def abs(a): return Vector3(abs(a.x), abs(a.y), abs(a.z))
    def sum(a): return a.x + a.y + a.z
    def scaled(a, b): return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)
    def min(a, b): return Vector3(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z))
    def max(a, b): return Vector3(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))
    def with_z(a, z): return Vector3(a.x, a.y, z)
    def dot(a, b): return a.x * b.x + a.y * b.y + a.z * b.z
    def magnitude(a): return math.sqrt(a.dot(a))
    def normalized(a): return a / a.magnitude()
    def round_to_int(a): return Vector3(round(a.x), round(a.y), round(a.z))

    def __str__(a): return f"({a.x}, {a.y}, {a.z})"
    def __repr__(a): return str(a)

    def __iter__(a): return iter((a.x, a.y, a.z))

@dataclass
class Hailstone:
    pos: Vector3
    vel: Vector3

    def eval(self, t: float) -> Vector3:
        return self.pos + self.vel * t

@dataclass
class InputData:
    hailstones: [Hailstone]

def parse_vector3(input: str) -> Vector3:
    x = input.split(', ')
    return Vector3(int(x[0]), int(x[1]), int(x[2]))

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    hailstones = []
    for line in lines:
        x = line.split(' @ ')
        hailstones.append(Hailstone(parse_vector3(x[0]), parse_vector3(x[1])))

    return InputData(hailstones)

def linesegment_intersect_2d(a1: Vector3, a2: Vector3, b1: Vector3, b2: Vector3) -> Vector3:
    det = (b2.y - b1.y) * (a2.x - a1.x) - (b2.x - b1.x) * (a2.y - a1.y)
    if det > -0.0001 and det < 0.0001: return None, None, None

    t1 = ((b2.x - b1.x) * (a1.y - b1.y) - (b2.y - b1.y) * (a1.x - b1.x)) / det
    t2 = ((a2.x - a1.x) * (a1.y - b1.y) - (a2.y - a1.y) * (a1.x - b1.x)) / det

    return t1, t2, a1 + (a2 - a1) * t1

def do_part1(input_data: InputData):
    hailstones = input_data.hailstones

    bounds_min, bounds_max = (7, 27) if IS_EXAMPLE else (200000000000000, 400000000000000)

    total_intersections = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            a = hailstones[i]
            b = hailstones[j]

            t1, t2, intersection = linesegment_intersect_2d(a.pos, a.pos + a.vel, b.pos, b.pos + b.vel)
            if intersection is None or t1 < 0 or t2 < 0: continue
            if intersection.x < bounds_min or intersection.x > bounds_max: continue
            if intersection.y < bounds_min or intersection.y > bounds_max: continue
            total_intersections += 1

    print(f"part1: {total_intersections}")

def calc_closest_encounter(s1: Hailstone, s2: Hailstone):
    a, b = s1.pos, s1.vel
    c, d = s2.pos, s2.vel
    e = a - c
    A = -b.dot(b) * d.dot(d) + math.pow(b.dot(d), 2)
    s = (-b.dot(b) * d.dot(e) + b.dot(e) * d.dot(b)) / A
    t = (d.dot(d) * b.dot(e) - d.dot(e) * d.dot(b)) / A
    # p1 = a + b * t
    # p2 = c + d * s
    # return p1, p2
    return s, (s1.eval(s) - s2.eval(s)).magnitude()

def test_calc_closest_encounter():
    test_hss = [
        [Hailstone(Vector3(6, 0, 3), Vector3(-2.5, 0, -1.5)), Hailstone(Vector3(3, 2, 2), Vector3(-1, -1, -1))],
        [Hailstone(Vector3(0, 0, 0), Vector3(1, 0, 0)), Hailstone(Vector3(0, 0, 0), Vector3(0, 1, 0))],
    ]

    for test_hs in test_hss:
        time, distance = calc_closest_encounter(test_hs[0], test_hs[1])
        point = test_hs[0].eval(time)
        print(f"{time=}, {distance=}, {point=}")
        assert(distance < 0.001)

def make_throw(a_time: float, a_pos: Vector3, b_time: float, b_pos: Vector3) -> Hailstone:
    if a_time > b_time:
        tmp_time, tmp_pos = a_time, a_pos
        a_time, a_pos = b_time, b_pos
        b_time, b_pos = tmp_time, tmp_pos

    try:
        vel = (b_pos - a_pos) / (b_time - a_time)
    except Exception as e:
        print(f"{a_time}, {b_time}")
        raise e
    start_pos = a_pos - vel * a_time
    return Hailstone(start_pos, vel)

def test_make_throw():
    a = Vector3(5, 0, 0)
    b = Vector3(5, 7, 0)
    throw = make_throw(2, a, 4, b)
    print(f"{throw}")

def calc_throw_error(throw: Hailstone, hailstones: [Hailstone]) -> float:
    total_error = 0
    for hs in hailstones:
        _, distance = calc_closest_encounter(throw, hs)
        total_error += distance
    return total_error

def find_best_times(a: Hailstone, b: Hailstone, others: [Hailstone], a_time_range: (float, float), b_time_range: (float, float), max_steps: int):
    best_result_error = None
    best_a_time = None
    best_b_time = None
    best_throw = None

    for a_i in tqdm(range(max_steps)):
        a_time = a_time_range[0] + (a_time_range[1] - a_time_range[0]) / (max_steps - 1) * a_i

        for b_i in range(max_steps):
            if b_i == a_i: continue
            b_time = b_time_range[0] + (b_time_range[1] - b_time_range[0])  / (max_steps - 1) * b_i

            throw = make_throw(a_time, a.eval(a_time), b_time, b.eval(b_time))
            error = calc_throw_error(throw, others)

            if best_result_error is None or error < best_result_error:
                best_result_error = error
                best_a_time = a_time
                best_b_time = b_time
                best_throw = throw

    return best_result_error, best_a_time, best_b_time, best_throw

def find_best_throw(a: Hailstone, b: Hailstone, others: [Hailstone], max_time: float) -> Hailstone:
    a_time_range = 0, max_time
    b_time_range = 0, max_time

    best_error = None
    best_throw = None
    for _ in range(10):
        max_steps = 1000
        error, a_time, b_time, throw = find_best_times(a, b, others, a_time_range, b_time_range, max_steps)

        print(f"{error=}")
        print(f"{throw=}")

        if best_error is not None and error >= best_error:
            break

        best_error = error
        best_throw = throw

        if best_error < 10: break

        range_divider = max_steps // 2

        atd = a_time_range[1] - a_time_range[0]
        a_time_range = (max(0, a_time - atd / range_divider), min(max_time, a_time + atd / range_divider))

        btd = b_time_range[1] - b_time_range[0]
        b_time_range = (max(0, b_time - btd / range_divider), min(max_time, b_time + btd / range_divider))

        print(f"{a_time_range=}, {b_time_range=}")

    return best_throw

def improve_best_throw(best_throw: Hailstone, others: [Hailstone]) -> (float, Hailstone):
    best_error = None
    best_offset = None

    for z in tqdm(range(-10, 10)):
        for y in range(-10, 10):
            for x in range(-10, 10):
                offset = Vector3(x, y, z)
                throw = Hailstone(best_throw.pos + offset, best_throw.vel)
                error = 0
                for hs in others:
                    _, distance = calc_closest_encounter(throw, hs)
                    error += distance

                if best_error is None or error < best_error:
                    best_error = error
                    best_offset = offset    

    print(f"{best_error=}, {best_offset=}")

    return best_error, Hailstone(best_throw.pos + best_offset, best_throw.vel)


def do_part2(input_data: InputData):

    hailstones = input_data.hailstones

    max_time = 10 if IS_EXAMPLE else 1000000000000

    # test_calc_closest_encounter()
    # test_make_throw()

    best_throw = find_best_throw(hailstones[1], hailstones[-1], hailstones[6:10], max_time)
    
    best_throw = Hailstone(best_throw.pos.round_to_int(), best_throw.vel.round_to_int())

    print(f"1st pass: {best_throw=}")

    best_error = None
    while True:
        error, throw = improve_best_throw(best_throw, hailstones[10:20])
        if best_error is not None and error >= best_error: break
        best_error = error
        best_throw = throw
        if error == 0: break

    print(f"2nd pass: {best_throw=}")

    print(f"part2: {best_throw.pos.x + best_throw.pos.y + best_throw.pos.z}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
