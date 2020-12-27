"""21. Allergens in foods."""
from collections import defaultdict
from copy import copy
from functools import reduce
from typing import DefaultDict, List, Set


def process_recipes(
    foods: List[str]
) -> (Set[str], DefaultDict[str, int], DefaultDict[str, Set[str]]):

    all_ingredients = set()
    for food in foods:
        ingredients, _ = food.split("(")
        all_ingredients = all_ingredients | set(ingredients.strip().split())

    could_contain_allergen = defaultdict(lambda: all_ingredients)
    ingredient_counts = defaultdict(int)
    for food in foods:

        ingredients, allergens = food.split("(")
        ingredients = set(ingredients.strip().split())
        for i in ingredients:
            ingredient_counts[i] += 1

        allergens = set(allergens.strip(")")[8:].strip().split(", "))

        for a in allergens:
            could_contain_allergen[a] = ingredients & could_contain_allergen[a]

    unseen_ingredients = all_ingredients - reduce(
        lambda a, b: a | b, could_contain_allergen.values()
    )

    return unseen_ingredients, ingredient_counts, could_contain_allergen


def part_one(
    unseen_ingredients: Set[str], ingredient_counts: DefaultDict[str, int]
) -> int:
    # count the number of appearances of ingredients that cannot contain allergens
    count = 0
    for i in unseen_ingredients:
        count += ingredient_counts[i]

    return count


def part_two(
    could_contain_allergen: DefaultDict[str, Set[str]]
) -> DefaultDict[str, str]:
    # resolve which allergen is in which ingredient
    n_allergens = len(could_contain_allergen.keys())
    ingredient_to_allergen = {}
    c = 0
    while c < n_allergens:
        for a, i in could_contain_allergen.items():
            if len(i) == 1:
                ingredient = i.pop()
                ingredient_to_allergen[ingredient] = a
                could_contain_allergen.pop(a)
                for b, j in could_contain_allergen.items():
                    could_contain_allergen[b].discard(ingredient)
                c += 1
                break
            else:
                continue

    return ",".join(
        sorted(ingredient_to_allergen, key=ingredient_to_allergen.__getitem__)
    )


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        foods = f.read().splitlines()

    unseen_ingredients, ingredient_counts, could_contain_allergen = process_recipes(
        foods
    )
    print(part_one(unseen_ingredients, ingredient_counts))
    print(part_two(could_contain_allergen))
