"""15. Elf game"""
from collections import defaultdict
from typing import List


def find_nth_number(initial_numbers: int, n: int) -> int:
    # find the 2020th number in the game
    memory = defaultdict(lambda: (None, None))
    number = None

    for i in range(n):

        if i < len(initial_numbers):
            number = initial_numbers[i]

        else:
            p, q = memory[number]

            if p is not None:
                number = (i - 1) - p
            else:
                number = 0

        memory[number] = (memory[number][1], i)

    return number


if __name__ == "__main__":

    initial_numbers = [6, 19, 0, 5, 7, 13, 1]
    print(find_nth_number(initial_numbers, 2020))
    print(find_nth_number(initial_numbers, 30_000_000))
