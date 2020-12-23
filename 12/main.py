"""12. Directing a ship."""
from collections import namedtuple
from math import cos, radians, sin
from typing import List

ShipState = namedtuple("ShipState", ["pos_x", "pos_y", "orientation"])
WorldState = namedtuple("WorldState", ["ship_x", "ship_y", "waypoint_x", "waypoint_y"])


def update_ship_state(ship_state: ShipState, instruction: str):
    # update the position and orientation of the ship given an instruction
    direction = instruction[0]
    distance = int(instruction[1:])

    if direction in ("W", "S", "R"):
        distance *= -1

    if direction == "E" or direction == "W":
        new_state = ShipState(
            pos_x=ship_state.pos_x + distance,
            pos_y=ship_state.pos_y,
            orientation=ship_state.orientation,
        )
    elif direction == "N" or direction == "S":
        new_state = ShipState(
            pos_x=ship_state.pos_x,
            pos_y=ship_state.pos_y + distance,
            orientation=ship_state.orientation,
        )
    elif direction == "F":
        new_state = ShipState(
            pos_x=ship_state.pos_x + distance * cos(radians(ship_state.orientation)),
            pos_y=ship_state.pos_y + distance * sin(radians(ship_state.orientation)),
            orientation=ship_state.orientation,
        )
    elif direction == "L" or direction == "R":
        new_state = ShipState(
            pos_x=ship_state.pos_x,
            pos_y=ship_state.pos_y,
            orientation=ship_state.orientation + distance,
        )

    return new_state


def update_world_state(world_state: WorldState, instruction: str) -> WorldState:
    # update waypoint and ship position given an instruction
    direction = instruction[0]
    distance = int(instruction[1:])

    if direction in ("W", "S", "R"):
        distance *= -1

    if direction == "N" or direction == "S":
        new_state = WorldState(
            ship_x=world_state.ship_x,
            ship_y=world_state.ship_y,
            waypoint_x=world_state.waypoint_x,
            waypoint_y=world_state.waypoint_y + distance,
        )
    elif direction == "E" or direction == "W":
        new_state = WorldState(
            ship_x=world_state.ship_x,
            ship_y=world_state.ship_y,
            waypoint_x=world_state.waypoint_x + distance,
            waypoint_y=world_state.waypoint_y,
        )
    elif direction == "L" or direction == "R":
        new_x = world_state.waypoint_x * cos(
            radians(distance)
        ) - world_state.waypoint_y * sin(radians(distance))
        new_y = world_state.waypoint_x * sin(
            radians(distance)
        ) + world_state.waypoint_y * cos(radians(distance))

        new_state = WorldState(
            ship_x=world_state.ship_x,
            ship_y=world_state.ship_y,
            waypoint_x=new_x,
            waypoint_y=new_y,
        )
    elif direction == "F":
        new_state = WorldState(
            ship_x=world_state.ship_x + distance * world_state.waypoint_x,
            ship_y=world_state.ship_y + distance * world_state.waypoint_y,
            waypoint_x=world_state.waypoint_x,
            waypoint_y=world_state.waypoint_y,
        )

    return new_state


def part_one(instructions: List[str]) -> int:
    # find the manhattan distance of the ship after executing the instructions
    ship_state = ShipState(pos_x=0, pos_y=0, orientation=0)

    for i in instructions:
        ship_state = update_ship_state(ship_state, i)

    return int(abs(ship_state.pos_x) + abs(ship_state.pos_y))


def part_two(instructions: List[str]) -> int:
    # same as above but for new rules in part two
    world_state = WorldState(ship_x=0, ship_y=0, waypoint_x=10, waypoint_y=1)

    for i in instructions:
        world_state = update_world_state(world_state, i)

    return int(abs(world_state.ship_x) + abs(world_state.ship_y))


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        instructions = f.readlines()

    print(part_one(instructions))
    print(part_two(instructions))
