#!/bin/python
from playsound import playsound
from argparse import ArgumentParser
from time import sleep, time
from datetime import datetime
from math import floor
import os
import sys


def log_brew(tea_type, tea_country):
    if not os.path.exists(os.path.expanduser("~/.drinks")):
        os.makedirs(os.path.expanduser("~/.drinks"), True)

    # format <timestamp>|<tea_type>|<tea_country>
    with open(os.path.expanduser('~/.drinks/tea.psv'), "a") as f:
        f.write(f'{datetime.fromtimestamp(time())}|{tea_type}|{tea_country}\n')


def main(args):
    if args.type not in ["puerh", "sheng", "shou", "black", "green", "white", "oolong", "herbal", "other"]:
        print(f"Warning: tea type {args.type} not recognized. Should I continue (y/n)?")

        input = sys.stdin.readline().lower().strip()
        if input != "y" and input != "yes":
            print("Exiting")
            sys.exit()

    log_brew(args.type, args.country)


def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("type", help="type of tea being brewed")
    parser.add_argument("country", help="country of tea being brewed")

    return parser.parse_args()

if __name__ == "__main__":
    main(_parse_args())