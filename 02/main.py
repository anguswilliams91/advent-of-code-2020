"""2. Check if passwords in a database are compliant with rules."""
from collections import Counter


def is_valid_password_old_rule(rule: str, password: str) -> bool:
    # check if a password is compliant with a rule
    letter_counts = Counter(password)

    count_constraint, letter = rule.split()
    lower, upper = map(int, count_constraint.split("-"))

    return (letter_counts[letter] >= lower) and (letter_counts[letter] <= upper)


def is_valid_password_new_rule(rule: str, password: str) -> bool:
    # check if a password is compliant with a rule from part 2
    indices, letter = rule.split()
    first, second = map(lambda i: int(i) - 1, indices.split("-"))

    return (password[first] == letter) != (password[second] == letter)


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        passwords = list(map(lambda p: p.strip().split(": "), f.readlines()))

    print(
        sum(is_valid_password_old_rule(rule, password) for rule, password in passwords)
    )
    print(
        sum(is_valid_password_new_rule(rule, password) for rule, password in passwords)
    )
