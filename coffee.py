#!/bin/python
from playsound import playsound
from argparse import ArgumentParser
from time import sleep, time
from datetime import datetime
from math import floor
import os
import sys

def print_in_place(s):
    print(s.ljust(40, ' '), end='\r')

def notification():
    playsound(os.path.expanduser("~/programming/caffeine-tracker/notification.mp3"))

def brew_finish(brew_time):
    logdir = os.path.expanduser("~/.drinks")
    if not os.path.exists(logdir):
        os.makedirs(logdir, True)

    # format <timestamp>|<brew_time>
    with open(f'{logdir}/coffee.psv', "a") as f:
        f.write(f'{datetime.fromtimestamp(time())}|{country}\n')


def main(args):
    # First, wait 30s to stir
    for t in range(30):
        print_in_place(f"Stir timer: {30 - t}s")
        sleep(1)

    notification()
    print("Stir the coffee!")

    # Then, brew for the specified time (default 2m30s)
    for t in range(args.brew_time):
        brew_mins = floor(args.brew_time / 60)
        mins_left = brew_mins - (t // 60)
        secs_left = (args.brew_time - t) % 60
        if mins_left > 0:
            print_in_place(f"\rBrew timer: {mins_left}m{secs_left}s")
        else:
            print_in_place(f"\rBrew timer: {secs_left}s")

        sleep(1)

    brew_finish(args.brew_time, args.country)
    notification()
    print("Done brewing!" + ' ' * 20)

def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("--brew-time",
    type=int,
    default=150,
    help="Time spent brewing after the initial pre-stir 30s")

    parser.add_argument("country", help="Origin country of coffee")

    return parser.parse_args()

if __name__ == "__main__":
    main(_parse_args())