"""1. Find the two numbers in a list that sum to 2020."""
from typing import List


def find_pair(expense_report: List[int]) -> int:
    """Return pair of inputs that sum to 2020.

    Args:
        expense_report (List[int]): list of integers.

    Returns:
        int: the product of the two numbers that sum to 2020.
    """
    sorted_expenses = sorted(expense_report)

    first = 0
    second = -1
    while (s := sorted_expenses[first] + sorted_expenses[second]) != 2020:
        if s < 2020:
            first += 1
        else:
            second -= 1

    return sorted_expenses[first] * sorted_expenses[second]


def find_triple(expense_report: List[int]) -> int:
    """Find triple of inputs that sum to 2020.

    Args:
        expense_report (List[int]): list of integers.

    Returns:
        int: the product of the three numbers that sum to 2020.
    """
    sorted_expenses = sorted(expense_report)
    n = len(sorted_expenses)

    for i in range(n):
        if i == 0 or sorted_expenses[i - 1] != sorted_expenses[i]:
            j, k = i + 1, n - 1
            while j < k:
                s = sorted_expenses[i] + sorted_expenses[j] + sorted_expenses[k]
                if s < 2020:
                    j += 1
                elif s > 2020:
                    k -= 1
                else:
                    return sorted_expenses[i] * sorted_expenses[j] * sorted_expenses[k]


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        expense_report = list(map(int, f.readlines()))

    print(find_pair(expense_report))
    print(find_triple(expense_report))
