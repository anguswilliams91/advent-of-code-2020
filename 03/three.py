"""3. Counting trees."""
from functools import reduce
from typing import List


def count_trees(terrain: List[List[str]], across: int, down: int) -> int:
    # count how many trees are encountered given a terrain and a slope
    height = len(terrain)
    width = len(terrain[0])
    num_trees = 0

    i, j = across, down
    while j < height:
        num_trees += terrain[j][i % width] == "#"
        j += down
        i += across

    return num_trees


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        terrain = list(map(lambda x: list(x.strip()), f.readlines()))

    print(count_trees(terrain, 3, 1))

    print(
        reduce(
            lambda x, y: x * y,
            map(
                lambda slope: count_trees(terrain, *slope),
                ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)),
            ),
        )
    )
