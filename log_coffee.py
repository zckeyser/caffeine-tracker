import os
from datetime import datetime
from time import time
from argparse import ArgumentParser


def brew_finish(country):
    logdir = os.path.expanduser("~/.drinks")
    if not os.path.exists(logdir):
        os.makedirs(logdir, True)

    # format <timestamp>|<brew_time>
    with open(f"{logdir}/coffee.psv", "a") as f:
        f.write(f'{datetime.fromtimestamp(time())}|{country}\n')


def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("country", help="Origin country of coffee")

    return parser.parse_args()

if __name__ == "__main__":
    brew_finish(_parse_args().country)