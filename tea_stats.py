from datetime import datetime, timedelta
from argparse import ArgumentParser
from os.path import expanduser
import os
import boto3

s3_client = boto3.client('s3')

class TeaSession():
    def __init__(self, timestamp, tea_type, tea_country):
        self.timestamp = timestamp
        self.type = tea_type
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
    tea_type = cols[1]
    tea_country = cols[2]

    return TeaSession(timestamp, tea_type, tea_country)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _s3_persist_file(func, file_name):
    filepath = f".tmp/{file_name}"

    os.makedirs(".tmp", True)

    # load file from s3 into temp file
    s3_client.download_file("caffeine-tracker", "tea.psv", filepath)

    # call function with location of file
    func(filepath)

    # copy back into s3
    upload_file(filepath)

    # remove temp file
    os.remove(filepath)


def main(args):
    data = None
    with open(expanduser(f"~/.drinks/tea.psv")) as f:
        data = [_parse_row(line) for line in f.readlines()]

    # base stats
    by_day = DataSet(lambda x: x.timestamp.date())
    by_type = DataSet(lambda x: x.type)
    by_country = DataSet(lambda x: x.country)
    for session in data:
        by_day.update(session)
        by_type.update(session)
        by_country.update(session)
    
    past_week_count = sum([cnt for date, (cnt, _) in by_day.items() if date >= datetime.now().date() - timedelta(days=7)])
    total_count = sum([cnt for date, (cnt, _) in by_day.items()])

    print("================= BASE STATS =====================")
    print()
    print(f"Cups of tea drank in the past week: {past_week_count}")
    print(f"Overall cups of tea drank: {total_count}")
    print()

    # verbose stats
    if args.v or args.vv:
        print("================= BY TYPE ====================")
        print()

        # print cups by type
        for tea_type, (cnt, _) in by_type.items():
            print(f"{tea_type}: {cnt}")

        print()
        print("================= BY COUNTRY =================")
        print()

        # print cups by country
        for country, (cnt, _) in by_country.items():
            print(f"{country}: {cnt}")

        print()

    # very verbose stats
    if args.vv:
        print("Not implemented yet!")

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