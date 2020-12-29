"""20. Seamonsters in images."""
from collections import defaultdict
from functools import reduce
from itertools import combinations
from typing import List, Dict, Set, Tuple

import numpy as np


class Tile:
    def __init__(self, tile_string: str):
        tile = tile_string.splitlines()
        self.id = int(tile[0].split()[1][:-1])
        self.image = np.array([[v == "#" for v in row] for row in tile[1:]], dtype=int)

    @property
    def edges(self) -> Set[Tuple[int]]:
        first_row = tuple(self.image[0, :])
        last_row = tuple(self.image[-1, :])
        first_column = tuple(self.image[:, 0])
        last_column = tuple(self.image[:, -1])
        return {first_row, last_row, first_column, last_column}

    @property
    def list_edges(self) -> Set[Tuple[int]]:
        first_row = tuple(self.image[0, :])
        last_row = tuple(self.image[-1, :])
        first_column = tuple(self.image[:, 0])
        last_column = tuple(self.image[:, -1])
        return [first_row, last_row, first_column, last_column]

    def reflect_up_down(self):
        # reflect the tile vertically
        self.image = self.image[::-1, :]

    def reflect_left_right(self):
        # reflect the tile horizontally
        self.image = self.image[:, ::-1]

    def rotate(self, n_turns: int):
        # rotate clockwise by 90 degrees ``n_turns`` times
        self.image = np.rot90(self.image, k=n_turns)

    def __str__(self):
        s = f"Tile {self.id}\n"
        v = " " + str(self.image)[1:-1]
        v = v.replace("0", ".").replace("1", "#").replace("[", "").replace("]", "")
        return s + v

    def __repr__(self):
        return str(self)


def find_possible_neighbours(tiles: Dict[int, np.ndarray]) -> Dict[int, Tuple[int]]:
    # for each tile, find tiles that could be its neighbour
    tile_to_neighbours = defaultdict(set)
    pairs = combinations(tiles.keys(), 2)
    for (i, j) in pairs:
        edges_i = tiles[i].edges | {e[::-1] for e in tiles[i].edges}
        edges_j = tiles[j].edges | {e[::-1] for e in tiles[j].edges}

        if edges_i & edges_j:
            tile_to_neighbours[i].add(j)
            tile_to_neighbours[j].add(i)
        else:
            pass

    return {t: tuple(n) for t, n in tile_to_neighbours.items()}


def build_image(tiles: Dict[int, Tile], tile_to_neighbours: Dict[int, int]):
    # build the image (assumes no dead ends)
    n_tiles = len(list(tiles.keys()))
    grid_size = int(n_tiles ** 0.5)
    id_grid = np.zeros((grid_size, grid_size), int)
    unresolved_ids = set()

    # pick one of the corner edges to start
    first_corner_id = [
        tile_id
        for tile_id, neighbours in tile_to_neighbours.items()
        if len(neighbours) == 2
    ][0]
    id_grid[0, 0] = first_corner_id

    first_corner = tiles[first_corner_id]
    neighbour_ids = tile_to_neighbours[first_corner_id]

    # find which edges are unmatched and orient the image so that these are top and left
    unmatched_edges = first_corner.edges
    for n in neighbour_ids:
        neighbour = tiles[n]
        other_edges = neighbour.edges | {e[::-1] for e in neighbour.edges}
        unmatched_edges = unmatched_edges - (unmatched_edges & other_edges)

    unmatched_indices = {
        first_corner.list_edges.index(unmatched_edges.pop()),
        first_corner.list_edges.index(unmatched_edges.pop()),
    }
    if unmatched_indices == {0, 3}:
        first_corner.rotate(1)
    elif unmatched_indices == {1, 3}:
        first_corner.rotate(2)
    elif unmatched_indices == {1, 2}:
        first_corner.reflect_up_down()
    else:
        pass

    id_grid[0, 0] = first_corner_id

    # now iteratively construct the grid
    current_id = first_corner_id
    unresolved_ids.add(first_corner_id)
    while 0 in id_grid:
        for neighbour in tile_to_neighbours[current_id]:
            if neighbour in id_grid:
                continue
            else:
                matched_edge = match_two_tiles(tiles[current_id], tiles[neighbour])

                ind = np.where(id_grid == current_id)
                (i, j) = (ind[0][0], ind[1][0])
                if matched_edge == 0:
                    id_grid[(i - 1, j)] = neighbour
                elif matched_edge == 1:
                    id_grid[(i + 1, j)] = neighbour
                elif matched_edge == 2:
                    id_grid[(i, j - 1)] = neighbour
                else:
                    id_grid[(i, j + 1)] = neighbour

                unresolved_ids.add(neighbour)

        current_id = unresolved_ids.pop()

    return id_grid


def match_two_tiles(static_tile: Tile, other_tile: Tile) -> int:
    # match two tiles, keeping one static and moving the other

    def check_match(matching_edges):
        matching_edge = matching_edges.pop()
        i = static_tile.list_edges.index(matching_edge)
        j = other_tile.list_edges.index(matching_edge)
        t = (i, j)
        if t in {(0, 1), (1, 0), (2, 3), (3, 2)}:
            return i
        else:
            return None

    for i in range(8):
        if i == 4:
            other_tile.reflect_left_right()
        other_tile.rotate(1)
        matching_edges = other_tile.edges & static_tile.edges

        if matching_edges:
            m = check_match(matching_edges)
            if m is not None:
                break
            else:
                continue

    return m


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        tiles_string = f.read().split("\n\n")

    tiles = {t.id: t for t in map(Tile, tiles_string)}

    # part one
    tile_to_neighbours = find_possible_neighbours(tiles)
    print(
        reduce(
            lambda a, b: a * b,
            {
                tile_id
                for tile_id, neighbours in tile_to_neighbours.items()
                if len(neighbours) == 2
            },
        )
    )

    # part two
    id_grid = build_image(tiles, tile_to_neighbours)
    print(id_grid)
