"""6. Counting number of positive responses in a survey."""
from collections import Counter


def count_answered_questions(group: str) -> int:
    # count the number of questions where at least one person answered yes
    return len(set(group.replace("\n", "")))


def count_completely_answered_questions(group: str) -> int:
    # count the number of questions where everyone answered yes
    num_people = len(group.split("\n"))
    question_counts = Counter(group.replace("\n", ""))

    return sum([answers == num_people for answers in question_counts.values()])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        text = f.read().strip()

    groups = text.split("\n\n")
    print(sum(count_answered_questions(group) for group in groups))
    print(sum(count_completely_answered_questions(group) for group in groups))
