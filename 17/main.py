"""17. Conway cubes.

1. Consider only neighbours of active cubes and active cubes because no other cubes
   can change state. 

"""
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import DefaultDict, List, Tuple


def get_neighbour_locations(dim: int) -> List[Tuple]:
    # get the relative positions of all neighbours of a point in a cartesian grid
    return [pos for pos in product(range(-1, 2), repeat=dim) if pos != (0,) * dim]


class CubeGrid:
    """A grid of Conway cubes."""

    def __init__(self, string_grid: List[List[str]], dim: int):
        self.dim = dim
        self.neighbour_pos = get_neighbour_locations(dim)

        self._update = self._update_3d if dim == 3 else self._update_4d

        grid = defaultdict(bool)
        for y in range(len(string_grid)):
            for x in range(len(string_grid[0])):
                grid[(x, y) + (0,) * (dim - 2)] = string_grid[y][x] == "#"
        self.grid = grid

    @property
    def active_cubes(self):
        # count the number of active cubes after six iterations
        for _ in range(6):
            self._update()

        return sum(self.grid.values())

    def _get_coord_ranges(self):
        # return the ranges of each coordinate that need to be scanned for updates
        coord_ranges = []
        for i in range(self.dim):
            c_range = sorted([p[i] for p in self.grid.keys()])
            c_lims = range(c_range[0] - 1, c_range[-1] + 2)
            coord_ranges.append(c_lims)

        return coord_ranges

    def _cube_state(self, p):
        # obtain the new state of a cube given the current state of all cubes
        num_active_neighbours = 0
        for q in self.neighbour_pos:
            neighbour_pos = tuple(p[i] + q[i] for i in range(self.dim))
            num_active_neighbours += self.grid[neighbour_pos]

        if self.grid[p]:
            new_state = 2 <= num_active_neighbours <= 3
        else:
            new_state = num_active_neighbours == 3

        return new_state

    def _update_3d(self):
        # update the grid in 3d
        x_range, y_range, z_range = self._get_coord_ranges()
        new_grid = defaultdict(bool)

        for x in x_range:
            for y in y_range:
                for z in z_range:
                    new_grid[(x, y, z)] = self._cube_state((x, y, z))

        self.grid = new_grid

    def _update_4d(self):
        # update the grid in 4d
        x_range, y_range, z_range, w_range = self._get_coord_ranges()
        new_grid = defaultdict(bool)

        for x in x_range:
            for y in y_range:
                for z in z_range:
                    for w in w_range:
                        new_grid[(x, y, z, w)] = self._cube_state((x, y, z, w))

        self.grid = new_grid


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        string_grid = list(map(list, f.read().splitlines()))

    cube_grid_3d = CubeGrid(string_grid, 3)
    cube_grid_4d = CubeGrid(string_grid, 4)

    print(cube_grid_3d.active_cubes)
    print(cube_grid_4d.active_cubes)
