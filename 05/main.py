"""5. Finding seats on a plane."""
from typing import List


def calculate_seat_number(seat: str) -> int:
    # calculate the seat number from the binary string representation
    row = seat[:7]
    column = seat[7:]

    row_number = int(row.replace("F", "0").replace("B", "1"), 2)
    column_number = int(column.replace("L", "0").replace("R", "1"), 2)

    return row_number * 8 + column_number


def find_missing_seat(seats: List[int]) -> int:
    # find the missing seat for which both adjacent seats are in the given list
    sorted_seats = sorted(seats)
    diffs = [1] + [s1 - s2 for s1, s2 in zip(sorted_seats[1:], sorted_seats[:-1])]
    return sorted_seats[diffs.index(2)] - 1


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        tickets = list(map(lambda x: x.strip(), f.readlines()))

    seats = [calculate_seat_number(ticket) for ticket in tickets]
    print(max(seats))
    print(find_missing_seat(seats))
