"""
Logs a session of coffee drinking, just some boilerplate to call log_session
"""
from argparse import ArgumentParser
from log_session import log_session

from s3_helper import s3_persist_file


def log_coffee_session(country, bucket_name):
    s3_persist_file(
        lambda filepath: log_session(filepath, country),
        'coffee.psv',
        bucket_name
    )


def _parse_args():
    parser = ArgumentParser()

    parser.add_argument("country", help="Origin country of coffee")
    parser.add_argument(
        "--bucket-name",
        help="Bucket to persist to in case you don't have a cached bucket"
        "and don't want to create a new one. Location of bucket cache is the file ~/.drinks/bucket.txt"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    log_coffee_session(args.country, args.bucket_name)
