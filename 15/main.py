"""15. Elf game"""
from collections import defaultdict, namedtuple
from typing import List


GameCounter = namedtuple("GameCounter", ["count", "spoken_at"])


def find_nth_number(initial_numbers: int, n: int) -> int:
    # find the 2020th number in the game
    memory = defaultdict(lambda: GameCounter(count=0, spoken_at=[None, None]))
    number = None

    for i in range(n):

        if i < len(initial_numbers):
            number = initial_numbers[i]

        else:
            if memory[number].count > 1:
                number = (i - 1) - memory[number].spoken_at[0]
            else:
                number = 0

        current_counter = memory[number]
        memory[number] = GameCounter(
            count=current_counter.count + 1,
            spoken_at=[current_counter.spoken_at[-1], i],
        )

    return number


if __name__ == "__main__":

    initial_numbers = [6, 19, 0, 5, 7, 13, 1]
    print(find_nth_number(initial_numbers, 2020))
    print(find_nth_number(initial_numbers, 30_000_000))
