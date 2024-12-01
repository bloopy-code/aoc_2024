"""Usefulish helper functions"""


def input_data_read(filepath: str):
    """read text file for puzzle inputs.

    Args:
        filepath (str): file path

    Returns:
        str: string of puzzle input?
    """
    with open(filepath, 'r', encoding="utf-8") as f:
        return f.read()


def rp(func):
    """Wrapper to return results in CLI.

    Args:
        func (function): plop it in.
    """
    def wrapper(*args, **kwargs):
        p1, p2 = func(*args, **kwargs)

        print("===== RESULTS =====")
        print(f"PART 1: {p1}")
        print(f"PART 2: {p2}")
        print('===================')

        return p1, p2
    return wrapper