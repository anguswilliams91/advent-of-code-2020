"""14. Bitmasks"""
from collections import defaultdict
from copy import deepcopy
from itertools import product
import re
from typing import Callable, Dict, List

MEM_ASSIGNMENT_REGEX = re.compile(r"mem\[(.*)\] = (.*)")
BITMASK_REGEX = re.compile(r"mask = (.*)")


def apply_bitmask_one(
    address: int, value: int, bitmask: str, memory: Dict[int, int]
) -> Dict[int, int]:
    # apply the bitmask to a decimal value, then convert back to decimal
    binary_value = list(bin(value)[2:].zfill(36))
    for ind, val in enumerate(bitmask):
        if val == "X":
            pass
        else:
            binary_value[ind] = val

    mutated_value = int("".join(binary_value), 2)
    memory[address] = mutated_value
    return memory


def apply_bitmask_two(
    address: int, value: int, bitmask: str, memory: Dict[int, int]
) -> Dict[int, int]:
    # use bitmask rule from the second part of the question
    binary_address = list(bin(address)[2:].zfill(36))

    for ind, val in enumerate(bitmask):
        if val == "0":
            pass
        elif val == "1":
            binary_address[ind] = "1"
        else:
            binary_address[ind] = "X"

    num_x = binary_address.count("X")
    possibilities = product(["0", "1"], repeat=num_x)
    x_indices = [i for (i, v) in enumerate(binary_address) if v == "X"]

    for possibility in possibilities:
        address = deepcopy(binary_address)

        for i, j in enumerate(x_indices):
            address[j] = possibility[i]

        mutated_address = int("".join(address), 2)
        memory[mutated_address] = value

    return memory


def execute_instructions(
    instructions: List[str],
    rule: Callable[[int, int, str, Dict[int, int]], Dict[int, int]],
) -> int:
    # execute the given instructions and then return sum of non-zero values in memory
    bitmask = None
    memory = defaultdict(int)

    for instruction in instructions:

        if m := BITMASK_REGEX.match(instruction):
            bitmask = m.groups()[0]

        else:
            m = MEM_ASSIGNMENT_REGEX.match(instruction)
            address, value = map(int, m.groups())
            memory = rule(address, value, bitmask, memory)

    return sum(memory.values())


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        instructions = list(map(lambda x: x.strip(), f.readlines()))

    print(execute_instructions(instructions, apply_bitmask_one))
    print(execute_instructions(instructions, apply_bitmask_two))
