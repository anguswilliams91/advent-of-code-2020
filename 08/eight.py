"""8. Breaking infinite loops in boot code."""
from collections import defaultdict, namedtuple
from copy import deepcopy
from typing import List, Tuple


ProgramState = namedtuple("ProgramState", ["acc", "current_line"])


def execute_instruction(instruction: str, program_state: ProgramState) -> ProgramState:
    # update the program's state given an instruction
    primitive, value = instruction.split()

    if primitive == "nop":
        new_state = ProgramState(
            acc=program_state.acc, current_line=program_state.current_line + 1
        )

    elif primitive == "acc":
        new_state = ProgramState(
            acc=program_state.acc + int(value),
            current_line=program_state.current_line + 1,
        )

    else:
        new_state = ProgramState(
            acc=program_state.acc, current_line=program_state.current_line + int(value)
        )

    return new_state


def run_program(instructions: List[str]) -> Tuple[int, bool]:
    # run a program and return accumulator, breaking as soon as there's a repeat
    n_instructions = len(instructions)
    evaluation_counts = defaultdict(int)
    program_state = ProgramState(acc=0, current_line=0)
    terminated_properly = True

    while program_state.current_line < n_instructions:

        instruction = instructions[program_state.current_line]
        evaluation_counts[program_state.current_line] += 1

        if evaluation_counts[program_state.current_line] > 1:
            terminated_properly = False
            break
        else:
            program_state = execute_instruction(instruction, program_state)

    return program_state.acc, terminated_properly


def adjust_program(instructions: List[str], index: int) -> List[str]:
    primitive, value = instructions[index].split()
    updated_instructions = deepcopy(instructions)

    if primitive == "nop":
        updated_instructions[index] = "jmp " + value
    elif primitive == "jmp":
        updated_instructions[index] = "nop " + value
    else:
        pass

    return updated_instructions


def fix_program(instructions: List[str]) -> int:
    # brute force search using lazy list
    adjusted_programs = (
        adjust_program(instructions, i) for i in range(len(instructions))
    )
    acc_at_termination = list(
        filter(lambda output: output[1], map(run_program, adjusted_programs))
    )[0][0]

    return acc_at_termination


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        instructions = list(map(lambda x: x.strip(), f.readlines()))

    print(run_program(instructions)[0])
    print(fix_program(instructions))
