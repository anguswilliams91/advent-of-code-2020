"""7. Count how many bags another bag can go be stored in."""
from collections import defaultdict
from typing import Dict, List, Tuple
import re

OUTER_BAG_REGEX = re.compile(r"([a-z]+ [a-z]+) bags contain ")
INNER_BAG_REGEX = re.compile(r"(\d) ([a-z]+ [a-z]+) bag[s]{0,1}[.,]{0,1}")


class BagGraph:
    """Directed graph with bag colours as nodes."""

    def __init__(self, rules: List[Dict[str, List[Tuple[int, str]]]]):
        self.bag_graph = defaultdict(set)

        for parent_to_children in rules:
            for parent, children in parent_to_children.items():
                for (_, child) in children:
                    self.insert(child, parent)

    def insert(self, x: str, y: str):
        self.bag_graph[x].add(y)

    def breadth_first_search(self, first: str) -> int:
        # standard bfs using a queue
        visited = defaultdict(bool)

        queue = [first]
        visited[first] = True

        while queue:
            current = queue.pop(0)
            for other in self.bag_graph[current]:
                if not visited[other]:
                    visited[other] = True
                    queue.append(other)

        return sum(visited.values())


def extract_rules_from_string(string_rules: List[str]) -> BagGraph:
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
    bag_graph = BagGraph(extract_rules_from_string(string_rules))
    return bag_graph.breadth_first_search("shiny gold") - 1


def count_inner_bags(rules: Dict[str, List[Tuple[int, str]]], colour):
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
