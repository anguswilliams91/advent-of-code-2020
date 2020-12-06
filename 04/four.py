"""4. Counting valid passports."""
from functools import reduce
import re
from typing import Callable

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
ECL_CHOICES = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

HCL_REGEX = re.compile(r"\#[0-9a-z]{6}")
PID_REGEX = re.compile(r"[0-9]{9}")
YEAR_REGEX = re.compile(r"[0-9]{4}")
HGT_REGEX = re.compile(r"\d+(in|cm)")

YEAR_LIMITS = {"byr": (1920, 2002), "iyr": (2010, 2020), "eyr": (2020, 2030)}


def contains_all_fields(passport: str) -> bool:
    # check a passport contains all the required fields
    return reduce(lambda x, y: x and y, (field + ":" in passport for field in FIELDS))


def contains_valid_data(passport: str) -> bool:
    # check that a passport contains valid data
    if not contains_all_fields(passport):
        return False

    key_vals = passport.split()
    for d in key_vals:
        field, data = d.split(":")

        if field in ("byr", "iyr", "eyr"):
            if not YEAR_REGEX.fullmatch(data):
                return False
            else:
                year = int(data)
                lower, upper = YEAR_LIMITS[field]
                if (year < lower) or (year > upper):
                    return False

        elif field == "hgt":
            if not HGT_REGEX.fullmatch(data):
                return False
            else:

                value = int(data[:-2])
                unit = data[-2:]

                if unit == "cm":
                    if (value < 150) or (value > 193):
                        return False
                elif unit == "in":
                    if (value < 59) or (value > 76):
                        return False

        elif field == "hcl":
            if not HCL_REGEX.fullmatch(data):
                return False

        elif field == "ecl":
            if data not in ECL_CHOICES:
                return False

        elif field == "pid":
            if not PID_REGEX.fullmatch(data):
                return False

        else:
            continue

    return True


def count_valid_passports(text: str, is_valid: Callable[[str], bool]) -> int:
    passports = text.split("\n\n")
    return sum(is_valid(passport) for passport in passports)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        text = f.read()

    print(count_valid_passports(text, contains_all_fields))
    print(count_valid_passports(text, contains_valid_data))
