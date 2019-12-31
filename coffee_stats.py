from datetime import datetime, timedelta
from argparse import ArgumentParser
from os.path import expanduser
import os
from s3_helper import s3_persist_file

class CoffeeSession():
    def __init__(self, timestamp, tea_country):
        self.timestamp = timestamp
        self.country = tea_country


class DataSet():
    def __init__(self, key_func=None):
        self.data = {}
        self.key_func = key_func if key_func else lambda x: x
    
    def __add__(self, other):
        self.update(other)

    def items(self):
        for k, v in self.data.items():
            yield (k, v)

    def update(self, item):
        key = self.key_func(item)
        if key in self.data:
            self.data[key][0] += 1
            self.data[key][1].append(item)
        else:
            self.data[key] = [1, [item]]


def _parse_row(row):
    cols = row.strip().split("|")

    timestamp = datetime.strptime(cols[0], "%Y-%m-%d %H:%M:%S.%f")
    coffee_country = cols[1]

    return CoffeeSession(timestamp, coffee_country)

def stats(filepath, verbose, very_verbose):
    data = None
    with open(filepath) as f:
        data = [_parse_row(line) for line in f.readlines()]

    # base stats
    by_day = DataSet(lambda x: x.timestamp.date())
    by_country = DataSet(lambda x: x.country)
    for session in data:
        by_day.update(session)
        by_country.update(session)
    
    past_week_count = sum([cnt for date, (cnt, _) in by_day.items() if date >= datetime.now().date() - timedelta(days=7)])
    total_count = sum([cnt for date, (cnt, _) in by_day.items()])

    print("================= BASE STATS =====================")
    print()
    print(f"Cups of coffee drank in the past week: {past_week_count}")
    print(f"Overall cups of coffee drank: {total_count}")
    print()

    # verbose stats
    if verbose or very_verbose:
        print()
        print("================= BY COUNTRY =================")
        print()

        # print sessions by country of origin
        for country, (cnt, _) in sorted(by_country.items(), key=lambda x: x[0]):
            print(f"{country}: {cnt}")

        print()

    # very verbose stats
    if very_verbose:
        pass

def main(args):
    s3_persist_file(
        lambda filepath: stats(filepath, args.v, args.vv),
        "coffee.psv"
    )

def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("-v",
                        default=False,
                        action='store_true',
                        help="moderate verbosity flag"
    )

    parser.add_argument("-vv",
                        default=False,
                        action='store_true',
                        help="full verbosity flag"
    )

    return parser.parse_args()

if __name__ == "__main__":
    main(_parse_args())