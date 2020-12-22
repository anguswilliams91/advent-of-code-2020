"""10. joltage adaptors."""
from functools import lru_cache
from typing import List


def calculate_differences(adaptors: List[int]) -> List[int]:
    # convert a list of adaptors into a list of differences in jolts
    sorted_adaptors = sorted(adaptors)
    sorted_adaptors = [0] + sorted_adaptors
    sorted_adaptors.append(sorted_adaptors[-1] + 3)
    return [a - b for a, b in zip(sorted_adaptors[1:], sorted_adaptors[:-1])]


def part_one(adaptors: List[int]) -> int:
    # find the product of the number of differences of size 1 and size 3
    differences = calculate_differences(adaptors)
    return differences.count(1) * differences.count(3)


@lru_cache
def number_of_subrun_orders(run_length: int) -> int:
    # the number of ways of ordering a set of adaptors with a one jolt differences
    if run_length <= 1:
        num_orders = 1
    elif run_length == 2:
        num_orders = 2
    else:
        num_orders = (
            number_of_subrun_orders(run_length - 3)
            + number_of_subrun_orders(run_length - 2)
            + number_of_subrun_orders(run_length - 1)
        )

    return num_orders


def part_two(adaptors: List[int]) -> int:
    # find number of possible orderings of adaptors
    start = 0
    number_of_orders = 1
    differences = calculate_differences(adaptors)
    n = len(differences)

    while start < n:
        if differences[start] == 3:
            start += 1
        else:
            end = start + 1
            while differences[end] == 1:
                end += 1
            number_of_orders *= number_of_subrun_orders(end - start)
            start = end

    return number_of_orders


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        adaptors = list(map(int, f.readlines()))

    print(part_one(adaptors))
    print(part_two(adaptors))
