"""19. Rules for messages."""
import re
from typing import Dict, List


def make_regex(rule: str, other_rules: Dict[str, str]) -> str:
    # make a regex from a rule
    reg = ""
    for p in rule.split(" "):
        if p in other_rules:
            # this rule needs to be further expanded
            reg += make_regex(rules[p], other_rules)
        else:
            # must be a or b, so just need to remove quotes
            reg += p.replace('"', "")

    if "|" in reg:
        # enclose "or" clauses with braces
        reg = "(" + reg + ")"

    return reg


def part_one(rules: Dict[str, str], messages: List[str]) -> int:
    # count the number of messages that match the rule
    reg = re.compile(make_regex(rules["0"], rules))
    return sum(bool(reg.fullmatch(message)) for message in messages)


def part_two(rules: Dict[str, str], messages: List[str], n_recursions: int) -> int:
    # find minimum number of recursions needed for given inputs
    # caved and used tom's solution...
    rules["8"] = "42 +"
    recursions = [" ".join(["42"] * _ + ["31"] * _) for _ in range(1, n_recursions)]
    rules["11"] = " | ".join(recursions)
    return part_one(rules, messages)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        notes = f.read()

    rules, messages = notes.split("\n\n")
    rules = dict(r.split(": ") for r in rules.splitlines())
    messages = messages.splitlines()

    print(part_one(rules, messages))
    print(part_two(rules, messages, 5))
