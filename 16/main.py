"""16. Validating ticket fields."""
from collections import namedtuple
from functools import reduce
import re
from typing import Dict, List, Tuple


CONSTRAINT_REGEX = re.compile(r"(.*): (.*) or (.*)")


TicketConstraints = Dict[str, List[Tuple[int, int]]]
Ticket = List[int]


def process_notes(
    raw_constraints: str, raw_my_ticket: str, raw_nearby_tickets: str
) -> (TicketConstraints, Ticket, List[Ticket]):
    # extract the data from the notes

    get_range = lambda raw_range: tuple(int(c) for c in raw_range.split("-"))
    constraints = {}
    for raw_constraint in raw_constraints.split("\n"):
        name, range_one, range_two = CONSTRAINT_REGEX.match(raw_constraint).groups()
        constraints[name] = [get_range(range_one), get_range(range_two)]

    process_ticket = lambda raw_ticket: [int(value) for value in raw_ticket.split(",")]

    my_ticket = process_ticket(raw_my_ticket.split("\n")[1])

    nearby_tickets = [
        process_ticket(raw_ticket) for raw_ticket in raw_nearby_tickets.split("\n")[1:]
    ]

    return constraints, my_ticket, nearby_tickets


def resolve_fields(possible_fields: List[Dict[str, bool]]) -> List[str]:
    # given a set of possible fields at each position, resolve which field is in each
    possible_fields = [
        {field for field, value in p.items() if value} for p in possible_fields
    ]
    n = len(possible_fields)
    fields = [None] * n

    converged = False
    while not converged:
        for i, p in enumerate(possible_fields):
            if len(p) == 1:
                fields[i] = p.pop()
                for j in range(n):
                    if j == i:
                        pass
                    else:
                        if possible_fields[j] and fields[i] in possible_fields[j]:
                            possible_fields[j].remove(fields[i])
                        else:
                            pass
            else:
                pass

            if all([x for x in fields]):
                converged = True

    return fields


def process_tickets(
    constraints: TicketConstraints, nearby_tickets: List[Ticket], my_ticket: Ticket
) -> int:
    # calculate part one and part two of the question

    n_fields = len(constraints.keys())
    error_rate = 0
    could_be_field = [
        {field: True for field in constraints.keys()} for _ in range(n_fields)
    ]
    for ticket in nearby_tickets:

        is_useable = True
        potential_fields = []
        for value in ticket:
            field_to_validity = {}
            is_valid = False

            for field, allowed_ranges in constraints.items():
                valid_for_this_field = reduce(
                    lambda a, b: a or b,
                    map(lambda x: x[0] <= value <= x[1], allowed_ranges),
                )
                field_to_validity[field] = valid_for_this_field
                is_valid = is_valid or valid_for_this_field

            error_rate += (not is_valid) * value
            potential_fields.append(field_to_validity)
            is_useable = is_useable and is_valid

        if is_useable:
            for overall, this_ticket in zip(could_be_field, potential_fields):
                for field, value in overall.items():
                    overall[field] = value and this_ticket[field]

    fields = resolve_fields(could_be_field)
    second_part = reduce(
        lambda a, b: a * b,
        (
            value
            for value, field in zip(my_ticket, fields)
            if field.startswith("departure")
        ),
    )

    return error_rate, second_part


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        notes = f.read().strip()

    raw_constraints, raw_my_ticket, raw_nearby_tickets = notes.split("\n\n")
    constraints, my_ticket, nearby_tickets = process_notes(
        raw_constraints, raw_my_ticket, raw_nearby_tickets
    )

    error_rate, second_part = process_tickets(constraints, nearby_tickets, my_ticket)
