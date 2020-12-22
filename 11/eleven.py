"""11. Seat occupation."""
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import List


@dataclass
class SeatMap:
    """Represent a map of seats that updates as passengers arrive."""
    seat_map: List[List[str]]

    def __post_init__(self):
        self.n_rows = len(self.seat_map)
        self.n_columns = len(self.seat_map[0])

    def iterate_to_terminal_state(self, rule_type: str = "first"):
        converged = False
        while not converged:
            previous_state = deepcopy(self.seat_map)
            self._update(rule_type)
            converged = self.seat_map == previous_state

    def __repr__(self):
        return "\n".join([" ".join(row) for row in self.seat_map])

    def _update(self, rule_type: str):
        new_map = deepcopy(self.seat_map)
        update_rule = (
            self._apply_first_rule if rule_type == "first" else self._apply_second_rule
        )

        for row in range(self.n_rows):
            for column in range(self.n_columns):
                new_map[row][column] = update_rule(self.seat_map, row, column)

        self.seat_map = new_map

    def _apply_first_rule(self, seat_map: List[List[str]], r: int, c: int) -> str:
        # apply update rule from first part of question
        seat_state = seat_map[r][c]

        if seat_state == ".":
            return seat_state

        neighbour_indices = [
            (i, j)
            for i in range(r - 1, r + 2)
            for j in range(c - 1, c + 2)
            if not (i == r and j == c)
            and i >= 0
            and j >= 0
            and i < self.n_rows
            and j < self.n_columns
        ]

        num_occupied_neigbours = 0
        for (i, j) in neighbour_indices:
            try:
                num_occupied_neigbours += seat_map[i][j] == "#"
            except IndexError:
                pass

        if num_occupied_neigbours == 0 and seat_state == "L":
            return "#"
        elif num_occupied_neigbours >= 4 and seat_state == "#":
            return "L"
        else:
            return seat_state

    def _apply_second_rule(self, seat_map: List[List[str]], r: int, c: int) -> str:
        # apply update rule from second part of question
        seat_state = seat_map[r][c]

        if seat_map == ".":
            return seat_state

        directions = list(
            filter(lambda x: x != (0, 0), product((-1, 0, 1), (-1, 0, 1)))
        )

        num_occupied_neigbours = 0
        for u, d in directions:
            s = 1
            while (
                0 <= (i := r + u * s) < self.n_columns
                and 0 <= (j := c + d * s) < self.n_rows
            ):
                if (n := seat_map[i][j]) != ".":
                    num_occupied_neigbours += n == "#"
                    break
                else:
                    s += 1

        if num_occupied_neigbours == 0 and seat_state == "L":
            return "#"
        elif num_occupied_neigbours >= 5 and seat_state == "#":
            return "L"
        else:
            return seat_state


def find_number_of_occupied_seats(seat_map: List[List[str]], rule_type: str) -> int:
    # find number of occupied seats once the seating process has completed
    seat_map = SeatMap(seat_map)
    seat_map.iterate_to_terminal_state(rule_type=rule_type)
    return sum(s == "#" for s in reduce(lambda a, b: a + b, seat_map.seat_map))


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        seat_map = list(map(lambda x: list(x.strip()), f.readlines()))

    print(find_number_of_occupied_seats(seat_map, "first"))
    print(find_number_of_occupied_seats(seat_map, "second"))
