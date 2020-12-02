"""2. Check if passwords in a database are compliant with rules."""
from collections import Counter


def is_valid_password_old_rule(rule: str, password: str) -> bool:
    """Check if a password is compliant with a rule.

    Rules are like: lower-upper character
    character must appear at least lower times and at most upper times.

    Args:
        rule (str): a string like "lower-upper character"
        password (str): a password containing only lower case letters

    Returns:
        bool: True if the password and rule are compatible
    """
    letter_counts = Counter(password)

    count_constraint, letter = rule.split()
    lower, upper = map(int, count_constraint.split("-"))

    return (letter_counts[letter] >= lower) and (letter_counts[letter] <= upper)


def is_valid_password_new_rule(rule: str, password: str) -> bool:
    """Check if a password is compliant with a rule.

    Rules are like: first_pos-second_pos character
    The character must appear in first_pos or second_pos, but not both.

    Args:
        rule (str): a string like "first_pos-second_pos character"
        password (str): a password containing only lower case letters

    Returns:
        bool: True if the password and rule are compatible
    """
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
