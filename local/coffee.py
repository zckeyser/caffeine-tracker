#!/bin/python
from argparse import ArgumentParser
from math import floor
import os

from playsound import playsound

from log_coffee import log_coffee_session


def print_in_place(s):
    print(s.ljust(40, ' '), end='\r')


def notification():
    # TODO use env var for this
    playsound(os.path.expanduser("~/programming/caffeine-tracker/notification.mp3"))


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
            print_in_place(f"Brew timer: {mins_left}m{secs_left}s")
        else:
            print_in_place(f"Brew timer: {secs_left}s")

        sleep(1)

    log_coffee_session(args.country, args.bucket_name)
    notification()
    print("Done brewing!" + ' ' * 20)


def _parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "--brew-time",
        type=int,
        default=150,
        help="Time spent brewing after the initial pre-stir 30s"
    )

    parser.add_argument(
        "--bucket-name",
        default=None,
        help="Bucket to base s3 persistence off of -- only need to pass once. If this is left empty and there is no cache at ~/.drinks/bucket.txt then this will create a new bucket."
    )

    parser.add_argument("country", help="Origin country of coffee")

    return parser.parse_args()


if __name__ == "__main__":
    main(_parse_args())
