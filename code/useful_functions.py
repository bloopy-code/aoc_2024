"""Usefulish helper functions"""
import time


def input_data_read(filepath: str):
    """Read text file for puzzle inputs.

    Args:
        filepath (str): file path

    Returns:
        str: string of puzzle input?
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def report_results(func):
    """Wrapper to return results in CLI.
    Now with timer!

    Args:
        func (function): plop it in.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        p1, p2 = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time

        print()
        print("===== RESULTS =====")
        print(f"PART 1: {p1}")
        print(f"PART 2: {p2}")
        print("-------------------")
        print(f"Time Taken: {total_time:.2f} seconds")
        print("===================")

        return p1, p2

    return wrapper
