"""22. Crab cards."""
from copy import copy
from typing import List, Set, Tuple


def parse_input(input_string: str) -> (List[int], List[int]):
    # extract the starting decks from the input
    deck_1, deck_2 = input_string.split("\n\n")
    deck_1 = [int(i) for i in deck_1.splitlines()[1:]]
    deck_2 = [int(i) for i in deck_2.splitlines()[1:]]
    return deck_1, deck_2


def play_combat(deck_1: List[int], deck_2: List[int]) -> (List[int], List[int]):
    # play the game until there's a winner
    is_a_winner = False
    while not is_a_winner:
        n_1 = deck_1.pop(0)
        n_2 = deck_2.pop(0)

        if n_1 > n_2:
            deck_1.extend([n_1, n_2])
        else:
            deck_2.extend([n_2, n_1])

        if not deck_1 or not deck_2:
            is_a_winner = True

    return deck_1, deck_2


def part_one(deck_1: List[int], deck_2: List[int]) -> int:
    # play the game and then return the winner's score
    n = len(deck_1) + len(deck_2)
    deck_1, deck_2 = play_combat(deck_1, deck_2)
    winners_deck = deck_1 or deck_2
    return sum(i * j for i, j in zip(range(1, n + 1), winners_deck[::-1]))


def play_recursive_combat(
    deck_1: List[int],
    deck_2: List[int],
    memory: Set[Tuple[Tuple[int], Tuple[int]]] = set(),
) -> (List[int], List[int]):
    # play the recursive version of the game

    is_a_winner = False
    while not is_a_winner:

        if (tuple(deck_1), tuple(deck_2)) in memory:
            is_a_winner = True

        else:
            memory.add((tuple(deck_1), tuple(deck_2)))

            n_1 = deck_1.pop(0)
            n_2 = deck_2.pop(0)

            if len(deck_1) >= n_1 and len(deck_2) >= n_2:
                sub_deck_1, sub_deck_2 = play_recursive_combat(
                    copy(deck_1[:n_1]), copy(deck_2[:n_2]), memory=set()
                )

                if (sub_deck_1 and sub_deck_2) or not sub_deck_2:
                    deck_1.extend([n_1, n_2])
                else:
                    deck_2.extend([n_2, n_1])

            else:
                if n_1 > n_2:
                    deck_1.extend([n_1, n_2])
                else:
                    deck_2.extend([n_2, n_1])

                if not deck_1 or not deck_2:
                    is_a_winner = True

    return deck_1, deck_2


def part_two(deck_1: List[int], deck_2: List[int]) -> int:
    # play the crab at recursive combat
    deck_1, deck_2 = play_recursive_combat(deck_1, deck_2)
    winners_deck = deck_1 if (deck_1 and deck_2) or not deck_2 else deck_2
    n = len(winners_deck)
    return sum(i * j for i, j in zip(range(1, n + 1), winners_deck[::-1]))


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        input_string = f.read()

    deck_1, deck_2 = parse_input(input_string)

    print(part_one(copy(deck_1), copy(deck_2)))
    print(part_two(copy(deck_1), copy(deck_2)))
