"""24. Hexagonal floor tiles."""
from collections import defaultdict
from functools import reduce
from typing import DefaultDict, List, Tuple, Set


def go_to_next_tile(instruction: str) -> Tuple[float, float]:
    # execute an instruction
    current_tile = (0, 0)
    i = 0

    while i < len(instruction):
        if (c := instruction[i]) in ("e", "w"):
            if c == "w":
                current_tile = (current_tile[0] - 1, current_tile[1])
            else:
                current_tile = (current_tile[0] + 1, current_tile[1])
            i += 1
        else:
            d = instruction[i : i + 2]
            if d == "ne":
                current_tile = (current_tile[0] + 0.5, current_tile[1] + 1)
            elif d == "nw":
                current_tile = (current_tile[0] - 0.5, current_tile[1] + 1)
            elif d == "se":
                current_tile = (current_tile[0] + 0.5, current_tile[1] - 1)
            else:
                current_tile = (current_tile[0] - 0.5, current_tile[1] - 1)
            i += 2

    return current_tile


def find_initial_floor(
    instructions: List[str],
) -> DefaultDict[Tuple[float, float], bool]:
    # find the number of black tiles remaining after executing the instructions
    floor = defaultdict(bool)

    for instruction in instructions:
        next_tile = go_to_next_tile(instruction)
        floor[next_tile] = not floor[next_tile]

    return floor


def get_neighbours(tile: Tuple[float, float]) -> Set[Tuple[float, float]]:
    # get the coordinates of a tile's neighbours
    return {
        (tile[0] + 1, tile[1]),
        (tile[0] - 1, tile[1]),
        (tile[0] + 0.5, tile[1] + 1),
        (tile[0] + 0.5, tile[1] - 1),
        (tile[0] - 0.5, tile[1] + 1),
        (tile[0] - 0.5, tile[1] - 1),
    }


def update_tile(
    tile: Tuple[float, float], floor: DefaultDict[Tuple[float, float], bool]
) -> bool:
    # update the state of a tile based on its neighbours
    num_active_neighbours = 0
    for neighbour in get_neighbours(tile):
        num_active_neighbours += floor[neighbour]

    if floor[tile]:
        new_state = not (num_active_neighbours == 0 or num_active_neighbours > 2)
    else:
        new_state = num_active_neighbours == 2

    return new_state


def update_art_exhibit(
    floor: DefaultDict[Tuple[float, float], bool]
) -> DefaultDict[Tuple[float, float], bool]:
    # do a single update of the art exhibit
    new_floor = defaultdict(bool)
    black_tiles = {location for location, colour in floor.items() if colour}
    tiles_to_update = reduce(
        lambda a, b: a | b, (get_neighbours(tile) for tile in black_tiles), black_tiles
    )

    for tile in tiles_to_update:
        new_floor[tile] = update_tile(tile, floor)

    return new_floor


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        instructions = f.read().splitlines()

    # part one
    floor = find_initial_floor(instructions)
    print(sum(floor.values()))

    # part two
    for _ in range(100):
        floor = update_art_exhibit(floor)
    print(sum(floor.values()))
