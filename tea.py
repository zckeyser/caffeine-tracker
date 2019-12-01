#!/bin/python
from playsound import playsound
from argparse import ArgumentParser
from time import sleep, time
from datetime import datetime
from math import floor
import os
import sys
from s3_helper import s3_persist_file

def log_brew(filepath, tea_type, tea_country):
    if not os.path.exists(os.path.expanduser("~/.drinks")):
        os.makedirs(os.path.expanduser("~/.drinks"), True)

    # format <timestamp>|<tea_type>|<tea_country>
    with open(filepath, "a") as f:
        f.write(f'{datetime.fromtimestamp(time())}|{tea_type}|{tea_country}\n')

def main(args):
    if args.type not in ["puerh", "sheng", "shou", "black", "green", "white", "oolong", "herbal", "other"]:
        print(f"Warning: tea type {args.type} not recognized. Should I continue (y/n)?")

        response = sys.stdin.readline().lower().strip()
        if response != "y" and response != "yes":
            print("Exiting")
            sys.exit()

    s3_persist_file(
        lambda filename: log_brew(filename, args.type, args.country),
        "tea.psv",
        args.bucket_name
    )


def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("type", help="type of tea being brewed")
    parser.add_argument("country", help="country of tea being brewed")
    parser.add_argument("--bucket-name", default=None, help="bucket in which logs are currently being stored. If not passed, a bucket name will be read from ~/.drinks/bucket.txt. If that file does not exist, a new bucket will be created")

    return parser.parse_args()

if __name__ == "__main__":
    main(_parse_args())