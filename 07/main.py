"""7. Count how many bags another bag can go be stored in."""
from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple
import re

OUTER_BAG_REGEX = re.compile(r"([a-z]+ [a-z]+) bags contain ")
INNER_BAG_REGEX = re.compile(r"(\d) ([a-z]+ [a-z]+) bag[s]{0,1}[.,]{0,1}")


def extract_rules_from_string(
    string_rules: List[str]
) -> List[Dict[str, List[Tuple[int, str]]]]:
    # extract the rules from the string representation
    rules = []
    for rule in string_rules:
        outer_bag = OUTER_BAG_REGEX.match(rule).groups(0)[0]
        inner_bags = [
            (int(quantity), colour)
            for (quantity, colour) in INNER_BAG_REGEX.findall(rule)
        ]
        rules.append({outer_bag: inner_bags})

    return rules


def count_possible_outer_bags(string_rules: List[str]) -> int:
    # part 1 - count number of possible outer bag colours
    rules = extract_rules_from_string(string_rules)

    bag_graph = defaultdict(set)
    for parent_to_children in rules:
        for parent, children in parent_to_children.items():
            for (_, child) in children:
                bag_graph[child].add(parent)

    # breadth first search
    queue = ["shiny gold"]
    visited = {"shiny gold"}

    while queue:
        current = queue.pop(0)
        for other in bag_graph[current]:
            if other not in visited:
                visited.add(other)
                queue.append(other)

    return len(visited) - 1


def count_inner_bags(rules: Dict[str, List[Tuple[int, str]]], colour: str) -> int:
    if not rules[colour]:
        return 0

    total = 0
    for (quantity, child) in rules[colour]:
        total += quantity * (1 + count_inner_bags(rules, child))

    return total


def count_bags_in_shiny_gold(string_rules: List[str]):
    # part 2 - count how many bags must be in the shiny gold bag
    rules = {
        k: v for z in extract_rules_from_string(string_rules) for k, v in z.items()
    }
    return count_inner_bags(rules, "shiny gold")


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        string_rules = f.readlines()

    print(count_possible_outer_bags(string_rules))
    print(count_bags_in_shiny_gold(string_rules))
