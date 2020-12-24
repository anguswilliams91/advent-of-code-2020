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


def eval_expression(expression: List[Union[int, str]], is_part_one: bool = True) -> int:
    # evaluate an expression using modified arithmetic from part one or two
    if len(expression) == 3:
        n, op, m = expression
        result = OPS[op](n, m)

    elif "(" in expression:
        loc_first_brace = expression.index("(")
        loc_closing_brace = find_closing_brace_index(loc_first_brace, expression)
        result = eval_expression(
            expression[:loc_first_brace]
            + [
                eval_expression(
                    expression[loc_first_brace + 1 : loc_closing_brace],
                    is_part_one=is_part_one,
                )
            ]
            + expression[loc_closing_brace + 1 :],
            is_part_one=is_part_one,
        )

    else:
        if is_part_one:
            # evaluate left to right
            result = eval_expression(
                [eval_expression(expression[:3], is_part_one)] + expression[3:]
            )
        else:
            # evaluate add before multiply
            try:
                loc_first_plus = expression.index("+")
                s = eval_expression(expression[loc_first_plus - 1 : loc_first_plus + 2])
                result = eval_expression(
                    expression[: loc_first_plus - 1]
                    + [s]
                    + expression[loc_first_plus + 2 :],
                    is_part_one=False,
                )
            except ValueError:
                result = eval_expression(expression)

    return result


if __name__ == "__main__":

    with open("input.txt", "r") as f:

        cases = list(map(lambda x: x.strip(), f.readlines()))

    processed_cases = list(map(preprocess_expression, cases))
    for is_part_one in (True, False):
        print(
            sum(
                eval_expression(case, is_part_one=is_part_one)
                for case in processed_cases
            )
        )
