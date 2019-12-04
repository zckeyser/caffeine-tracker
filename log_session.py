from datetime import datetime
from time import time


def log_session(filepath, *args):
    with open(filepath, "a") as f:
        cols = "|".join(args)
        f.write(f"{datetime.fromtimestamp(time())}|{cols}\n")
