"""23. Crab cups."""
from typing import List


class CrabCups:
    """The game of crab cups, represented as a linked list."""
    def __init__(self, cups: List[int]):
        self.max_cup = max(cups)
        self.n = len(cups)
        self.cups = {cup: next_cup for cup, next_cup in zip(cups[:-1], cups[1:])}
        self.cups[cups[-1]] = cups[0]
        self.current_cup = cups[0]

    def play_round(self):
        destination_cup = (
            self.current_cup - 1 if (self.current_cup - 1) > 0 else self.max_cup
        )
        pickup_cups = (
            self.cups[self.current_cup],
            self.cups[self.cups[self.current_cup]],
            self.cups[self.cups[self.cups[self.current_cup]]],
        )

        while destination_cup in pickup_cups:
            destination_cup = (
                destination_cup - 1 if destination_cup - 1 > 0 else self.max_cup
            )

        dest_next = self.cups[destination_cup]
        self.cups[destination_cup] = pickup_cups[0]
        self.cups[self.current_cup] = self.cups[pickup_cups[2]]
        self.cups[pickup_cups[2]] = dest_next
        self.current_cup = self.cups[self.current_cup]

    def play_game(self, n_rounds: int):
        for _ in range(n_rounds):
            self.play_round()

    def __str__(self):
        cups = ""
        current = 1
        while (c := self.cups[current]) != 1:
            cups += str(c)
            current = c

        return cups

    def __getitem__(self, cup_label: int) -> int:
        return self.cups[cup_label]


if __name__ == "__main__":

    cup_labels = "284573961"
    initial_cups = list(map(int, list(cup_labels)))

    # part one
    cups = CrabCups(initial_cups)
    cups.play_game(100)
    print(cups)

    # part two
    second_cups = initial_cups + list(range(cups.max_cup + 1, 1_000_001))
    big_cups = CrabCups(second_cups)
    big_cups.play_game(10_000_000)
    print(big_cups[1] * big_cups[big_cups[1]])
