"""13. Bus arrivals."""
from functools import reduce
from typing import List


def waiting_time(earliest_time: int, bus_number: int) -> int:
    return bus_number - earliest_time % bus_number


def find_earliest_bus(earliest_time: int, buses: List[int]) -> int:
    # find the bus ID multiplied by the waiting time for the bus that arrives first

    best_bus = None
    min_time = float("inf")
    for bus in buses:
        t = waiting_time(earliest_time, bus)
        if t < min_time:
            min_time = t
            best_bus = bus

    return best_bus * min_time


def win_gold_coin(buses: List[int]) -> int:
    # chinese remainder theorem, using page from brilliant.org
    # no chance on this one, turned to reddit!
    buses = [(i, b) for i, b in enumerate(buses) if b != "x"]
    N = reduce(lambda a, b: a * b, (bus[1] for bus in buses))
    return sum(-ai * pow(N // ni, -1, ni) * (N // ni) for (ai, ni) in buses) % N


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        earliest_time = int(f.readline().strip())
        buses = [
            int(bus) if bus != "x" else bus for bus in f.readline().strip().split(",")
        ]

    filtered_buses = [bus for bus in buses if bus != "x"]
    print(find_earliest_bus(earliest_time, filtered_buses))
    print(win_gold_coin(buses))

