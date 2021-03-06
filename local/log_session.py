"""
used to log arbitrary columns to a .psv file in the correct format with a timestamp prepended
"""
from datetime import datetime
from time import time


def log_session(filepath, *args):
    with open(filepath, "a") as f:
        cols = "|".join(args)
        f.write(f"{datetime.fromtimestamp(time())}|{cols}\n")
