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
class Condition:
    attr: int
    is_less: bool
    value: int

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Part:
    attrs: Tuple[int]

@dataclass
class Workflow:
    rules: List[Tuple[Condition, str]]
    default_rule: str

@dataclass
class InputData:
    workflows: Dict[str, Workflow]
    parts: [Part]

def attr_to_int(attr: str) -> int:
    match attr:
        case "x": return 0
        case "m": return 1
        case "a": return 2
        case "s": return 3

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    parsing_workflows = True
    workflows = {}
    parts = []
    for line in lines:
        if parsing_workflows:
            if len(line) == 0: 
                parsing_workflows = False
                continue
            str_parts1 = line.split('{')
            workflow_name = str_parts1[0]
            str_parts2 = str_parts1[1][:-1].split(',')
            default_rule = str_parts2[-1]
            rules = []
            for rule_str in str_parts2[:-1]:
                rule_parts = rule_str.split(':')
                cond_str = rule_parts[0]
                cmp_idx = max(cond_str.find('<'), cond_str.find('>'))
                rules.append((
                    Condition(attr_to_int(cond_str[:cmp_idx]), cond_str[cmp_idx] == '<', int(cond_str[cmp_idx + 1:])), 
                    rule_parts[1]
                ))
            workflows[workflow_name] = Workflow(rules, default_rule)
        else:
            str_parts = line[1:-1].split(',')
            attrs = [0] * 4
            for attr_str in str_parts:
                attr_str_parts = attr_str.split('=')
                attrs[attr_to_int(attr_str_parts[0])] = int(attr_str_parts[1])
            parts.append(Part(tuple(attrs)))

    return InputData(workflows, parts)

def check_part_condition(part: Part, condition: Condition):
    part_value = part.attrs[condition.attr]
    return part_value < condition.value if condition.is_less else part_value > condition.value

def do_part1(input_data: InputData):
    accepted_parts = []

    for part in input_data.parts:
        cur_workflow = input_data.workflows["in"]
        while True:
            for condition, target_name in cur_workflow.rules:
                if check_part_condition(part, condition):
                    break
            else:
                target_name = cur_workflow.default_rule

            if target_name == "A":
                accepted_parts.append(part)
                break
            elif target_name == "R":
                break

            cur_workflow = input_data.workflows[target_name]

    accepted_sums = [sum(part.attrs) for part in accepted_parts]
    print(f"part1: {sum(accepted_sums)}")

@dataclass(slots=True, frozen=True, eq=True, order=True)
class InclusiveRange:
    min: int
    max: int

    def split_less(self, at: int) -> (Self, Self):
        return (
            InclusiveRange(self.min, min(self.max, at - 1)) if self.min < at else None, 
            InclusiveRange(max(self.min, at), self.max) if self.max >= at else None
        )

@dataclass(slots=True, frozen=True, eq=True, order=True)
class PartsRange:
    attrs: Tuple[InclusiveRange]

    def get_combinations_count(self):
        return functools.reduce(operator.mul, [r.max - r.min + 1 for r in self.attrs], 1)
    
    def with_attr_range(self, attr: int, range: InclusiveRange):
        return PartsRange(self.attrs[:attr] + (range,) + self.attrs[attr + 1:])

def rec_solve_part2(workflows: Dict[str, Workflow], cur_workflow_name: str, cur_range: PartsRange) -> int:
    cur_workflow = workflows[cur_workflow_name]
    total_accepted = 0

    for condition, target_name in cur_workflow.rules + [(Condition(0, False, -1), cur_workflow.default_rule)]:
        attr_range = cur_range.attrs[condition.attr]
        if condition.is_less:
            true_attr_range, false_attr_range = attr_range.split_less(condition.value)
        else:
            false_attr_range, true_attr_range = attr_range.split_less(condition.value + 1)

        if true_attr_range is not None:
            true_range = cur_range.with_attr_range(condition.attr, true_attr_range)

            if target_name == "A":
                total_accepted += true_range.get_combinations_count()
            elif target_name != "R":
                total_accepted += rec_solve_part2(workflows, target_name, true_range)
            
        if false_attr_range is None: 
            break
        cur_range = cur_range.with_attr_range(condition.attr, false_attr_range)

    return total_accepted

def do_part2(input_data: InputData):
    start_range = PartsRange(tuple([InclusiveRange(1, 4000)] * 4))
    total_accepted = rec_solve_part2(input_data.workflows, "in", start_range)
    print(f"part2: {total_accepted}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
