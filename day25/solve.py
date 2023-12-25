from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math
# import graphviz

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

@dataclass
class InputData:
    node_names: [str]
    connections: [(str, str)]

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    nodes = set()
    for line in lines:
        x = line.split(": ")
        nodes.add(x[0])
        for dst in x[1].split(" "):
            nodes.add(dst)

    connections = []
    for line in lines:
        x = line.split(": ")
        src = x[0]
        for dst in x[1].split(" "):
            connections.append((src, dst))

    return InputData(node_names=list(nodes), connections=connections)

# def draw_graph(nodes, connections):
#     dot = graphviz.Graph(comment='Graph')

#     for node in nodes:
#         dot.node(node, node)

#     for connection in connections:
#         dot.edge(str(connection[0]), str(connection[1]), label=str(""))

#     dot.render('graph.gv').replace('\\', '/')

# def draw_graph2(connections_map, node_levels):
#     dot = graphviz.Graph(comment='Graph')

#     for src_idx in connections_map.keys():
#         dot.node(str(src_idx), f"{src_idx} ({node_levels[src_idx]})")

#     conn_added = set()
#     for src_idx in connections_map.keys():
#         for conn_idx, dst_idx in connections_map[src_idx]:
#             if conn_idx in conn_added: continue
#             conn_added.add(conn_idx)
#             dot.edge(str(src_idx), str(dst_idx), label=str(conn_idx))

#     dot.render('graph2.gv').replace('\\', '/')

def flow_step(connections_map, node_levels, connections_used) -> bool:
    total_flow = 0
    for src_idx in range(len(node_levels)):
        for conn_idx, dst_idx in connections_map[src_idx]:
            if not connections_used[conn_idx] and node_levels[src_idx] > node_levels[dst_idx] + 1:
                node_levels[src_idx] -= 1
                node_levels[dst_idx] += 1
                connections_used[conn_idx] = True
                total_flow += 1
    return total_flow > 0

def do_part1(input_data: InputData):
    node_names = input_data.node_names
    connections = input_data.connections

    # draw_graph(input_data.node_names, input_data.connections)

    node_idx_map = {}
    for i, name in enumerate(node_names):
        node_idx_map[name] = i

    connections_map = {i: [] for i, _ in enumerate(node_names)}
    for conn_idx, connection in enumerate(connections):
        src_idx = node_idx_map[connection[0]]
        dst_idx = node_idx_map[connection[1]]
        connections_map[src_idx].append((conn_idx, dst_idx))
        connections_map[dst_idx].append((conn_idx, src_idx))

    nodes_sorted_by_connections = sorted(node_names, key=lambda name: len(connections_map[node_idx_map[name]]), reverse=True)

    for origin_node_name in nodes_sorted_by_connections:
        node_levels = [0] * len(node_names)
        connections_used = [False] * len(connections)

        node_levels[node_idx_map[origin_node_name]] = 100000
        max_steps = 10000
        for step in tqdm(range(max_steps)):
            for i in range(len(connections_used)): connections_used[i] = False
            while flow_step(connections_map, node_levels, connections_used):
                pass

        # draw_graph2(connections_map, node_levels)
        sorted_levels = sorted(node_levels)

        for i in range(1, len(node_names) - 1):
            if sorted_levels[i] - sorted_levels[i - 1] > 30:
                group1_count = i
                group2_count = len(node_names) - i
                break
        else:
            continue
        break
    
    print(f"{group1_count=}, {group2_count=}")
    print(f"part1: {group1_count * group2_count}")

def do_part2(input_data: InputData):
    print(f"part2: big red button pressed")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
