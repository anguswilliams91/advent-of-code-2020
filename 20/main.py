"""20. Rebuilding a camera array."""
from collections import defaultdict
from copy import deepcopy
from functools import reduce
from itertools import combinations
from typing import Dict, List, Set

EDGE_INDICES = ((0, None), (-1, None), (None, 0), (None, -1))


def make_tile(tile_string: str) -> List[List[bool]]:
    tile = tile_string.splitlines()
    tile_id = int(tile[0].split()[1][:-1])

    tile_values = [[v == "#" for v in row] for row in tile[1:]]

    return tile_id, tile_values


def make_tiles(tiles_string: List[str]) -> Dict[int, List[List[bool]]]:
    return {tile_id: value for (tile_id, value) in map(make_tile, tiles_string)}


def part_one(tiles: Dict[int, List[List[bool]]]) -> Dict[int, Set[int]]:
    # find the corner tiles - these are tiles where only two edges match edges in other tiles...maybe
    edge_matches = defaultdict(set)
    edges = defaultdict(set)

    for i, tile in tiles.items():
        es = set()

        for p, q in EDGE_INDICES:
            if p is None:
                e = [tile[_][q] for _ in range(10)]
            else:
                e = tile[p]

            es.add(tuple(e))
            es.add(tuple(reversed(e)))
        edges[i] = es

    for i, tile in tiles.items():
        for j, tile in tiles.items():
            if i == j:
                pass
            else:
                edge_matches[i] = edge_matches[i] | (edges[i] & edges[j])

    corners = [i for i, v in edge_matches.items() if len(v) // 2 == 2]

    return reduce(lambda a, b: a * b, corners)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        tiles_string = f.read().split("\n\n")

    tiles = make_tiles(tiles_string)
    print(part_one(tiles))
