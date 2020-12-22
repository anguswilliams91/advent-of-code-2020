"""9. XMAS cipher."""
from typing import List


def find_illegal_entry(numbers: List[int], preamble_size: int) -> int:
    # find the first illegal entry in a list

    for current_index in range(preamble_size, len(numbers)):
        preamble = numbers[(current_index - preamble_size) : current_index]
        preamble_set = set(preamble)
        current_value = numbers[current_index]

        if preamble.count(current_value / 2) == 1:
            # case when current value is double a unique element in the preamble
            preamble_set.remove(current_value / 2)

        is_valid = False
        other_ind = 0
        while (not is_valid) and (other_ind < len(preamble)):
            if (current_value - preamble[other_ind]) in preamble_set:
                is_valid = True
            other_ind += 1

        if not is_valid:
            break

    return current_value


def find_encryption_weakness(numbers: List[int], target: int) -> int:
    # find min and max values in contiguous set that sums to target
    n = len(numbers)
    start = -1
    found_solution = False

    while not found_solution:
        start += 1
        running_sum = 0

        for end in range(start, n):
            running_sum += numbers[end]
            if running_sum == target:
                found_solution = True
                break
            elif running_sum > target:
                break

    sorted_subset = sorted(numbers[start : (end + 1)])
    return sorted_subset[0] + sorted_subset[-1]


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        numbers = list(map(int, f.readlines()))

    illegal_entry = find_illegal_entry(numbers, 25)
    print(illegal_entry)

    print(find_encryption_weakness(numbers, illegal_entry))
