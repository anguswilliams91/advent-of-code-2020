"""Utility to run solutions."""
from argparse import ArgumentParser
import os
import time
import pathlib
from typing import Union

BASE_PATH = pathlib.Path(__file__).parent.absolute()


def run_day(day: int):
    # run the given day
    if int(day) not in range(1, 26):
        raise ValueError("day must be between 1 and 25!")

    print(f"Running day {day}.")
    start = time.time()
    solution_dir = BASE_PATH / str(day).zfill(2)
    os.chdir(solution_dir)
    os.system("python main.py")
    end = time.time()
    print(f"Took {end - start: .2f} seconds.\n")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(dest="day", help="Run the solution to this day of AOC.")
    args = parser.parse_args()

    if args.day != "all":
        run_day(args.day)

    else:
        overall_start = time.time()
        for day in range(1, 26):
            run_day(day)
        overall_end = time.time()
        print(f"Total time taken: {overall_end - overall_start: .1f} seconds.")
