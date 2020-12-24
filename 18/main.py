"""18. Weird maths."""
from typing import List, Union

OPS = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}


def preprocess_expression(expression: str) -> List[Union[int, str]]:
    # preprocess a string expression before evaluating it
    expression = expression.replace(" ", "")
    processed_expression = []
    for e in expression:
        try:
            processed_expression.append(int(e))
        except ValueError:
            processed_expression.append(e)

    return processed_expression


def find_closing_brace_index(open_ind: int, expression: List[Union[int, str]]) -> int:
    # find the index of a matching brace given the position of an opening brace
    subset = expression[open_ind + 1 :]
    open_braces = 0
    for i, e in enumerate(subset):

        if e == ")":
            if not open_braces:
                closing_ind = open_ind + 1 + i
                break
            else:
                open_braces -= 1

        elif e == "(":
            open_braces += 1

        else:
            continue

    return closing_ind


def eval_expression(expression: List[Union[int, str]]) -> int:
    # evaluate an expression
    if len(expression) == 3:
        n, op, m = expression
        result = OPS[op](n, m)

    elif "(" in expression:
        loc_first_brace = expression.index("(")
        loc_closing_brace = find_closing_brace_index(loc_first_brace, expression)
        result = eval_expression(
            expression[:loc_first_brace]
            + [eval_expression(expression[loc_first_brace + 1 : loc_closing_brace])]
            + expression[loc_closing_brace + 1 :]
        )

    else:
        result = eval_expression([eval_expression(expression[:3])] + expression[3:])

    return result


if __name__ == "__main__":

    with open("input.txt", "r") as f:

        cases = list(map(lambda x: x.strip(), f.readlines()))

    processed_cases = map(preprocess_expression, cases)
    part_one = 0
    for case in processed_cases:
        part_one += eval_expression(case)

    print(part_one)
