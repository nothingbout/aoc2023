from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Any, Self
from tqdm import tqdm
import operator
import functools
import itertools
import math

IS_EXAMPLE = False
INPUT_FILE = "example2.txt" if IS_EXAMPLE else "input.txt"

@dataclass(slots=True)
class Module:
    name: str
    type: str
    dst_names: [str]
    src_names: [str]

@dataclass
class InputData:
    modules: Module

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    modules = {}
    all_dst_names = []
    for line in lines:
        parts = line.split(' -> ')
        if parts[0] == "broadcaster":
            mod_type = parts[0]
            mod_name = parts[0]
        else:
            mod_type = parts[0][0]
            mod_name = parts[0][1:]
        mod_dst_names = parts[1].split(', ')
        modules[mod_name] = Module(mod_name, mod_type, mod_dst_names, [])
        all_dst_names.extend(mod_dst_names)

    for dst_name in all_dst_names:
        if not dst_name in modules:
            modules[dst_name] = Module(dst_name, "", [], [])

    for src_mod in modules.values():
        for dst_name in src_mod.dst_names:
            modules[dst_name].src_names.append(src_mod.name)

    return InputData(modules=modules)

@dataclass(slots=True, frozen=True, eq=True, order=True)
class ModuleState:
    values: Tuple[bool]

    def new_state(mod: Module):
        match mod.type:
            case "%": return ModuleState((False,))
            case "&": return ModuleState((False,) * len(mod.src_names))
        return ModuleState(values=())
    
    def with_value(self, idx: int, value: bool):
        return ModuleState(self.values[:idx] + (value,) + self.values[idx + 1:])
    
    def all_high(self) -> bool:
        return False not in self.values

@dataclass(slots=True, frozen=True, eq=True, order=True)
class Signal:
    src: str
    dst: str
    value: bool

def apply_signal(mod: Module, state: ModuleState, signal: Signal) -> (ModuleState, bool):
    new_state = state
    output_signal = None

    match mod.type:
        case "%":
            if not signal.value:
                new_value = not state.values[0]
                new_state = state.with_value(0, new_value)
                output_signal = new_value
        case "&":
            src_idx = mod.src_names.index(signal.src)
            new_state = state.with_value(src_idx, signal.value)
            output_signal = False if new_state.all_high() else True
        case "broadcaster":
            output_signal = signal.value

    return new_state, output_signal

def process_signal(modules, mod_states, signals, signal):
    cur_mod = modules[signal.dst]
    cur_state = mod_states[cur_mod.name]

    new_state, output_signal_value = apply_signal(cur_mod, cur_state, signal)
    mod_states[cur_mod.name] = new_state
    if output_signal_value is not None:
        for dst_name in cur_mod.dst_names:
            signals.append(Signal(cur_mod.name, dst_name, output_signal_value))

def do_part1(input_data: InputData):
    modules = input_data.modules
    mod_states = { mod.name: ModuleState.new_state(mod) for mod in modules.values() }

    low_signals_popped = 0
    high_signals_popped = 0

    for step in range(1000):
        signals = [Signal("button", "broadcaster", False)]

        while len(signals) > 0:
            signal = signals.pop(0)

            if signal.value: high_signals_popped += 1
            else: low_signals_popped += 1

            process_signal(modules, mod_states, signals, signal)

    print(f"part1: {low_signals_popped * high_signals_popped}")

def button_presses_for_signal(modules, target_dst, target_value):
    mod_states = { mod.name: ModuleState.new_state(mod) for mod in modules.values() }

    button_presses = None
    for step in range(10000000000):
        signals = [Signal("button", "broadcaster", False)]

        while len(signals) > 0:
            signal = signals.pop(0)
            if signal.dst == target_dst:
                if signal.value == target_value:
                    button_presses = step + 1
                    break
            process_signal(modules, mod_states, signals, signal)
        
        if button_presses is not None:
            break
    return button_presses

def do_part2(input_data: InputData):
    modules = input_data.modules

    target_modules = modules[modules["rx"].src_names[0]].src_names

    press_counts = []
    for name in target_modules:
        press_counts.append(button_presses_for_signal(modules, name, False))

    needed_presses = functools.reduce(operator.mul, press_counts, 1)

    print(f"part2: {needed_presses}")

if __name__ == '__main__':
    start_time = datetime.now()
    input_data = parse_input()

    do_part1(input_data)
    do_part2(input_data)

    end_time = datetime.now()
    print(f"run time: {end_time - start_time}")
