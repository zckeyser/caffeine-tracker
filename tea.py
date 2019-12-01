#!/bin/python
from playsound import playsound
from argparse import ArgumentParser
from time import sleep, time
from datetime import datetime
from math import floor
import os
import sys
import boto3
import logging
from uuid import uuid4

def log_brew(filepath, tea_type, tea_country):
    if not os.path.exists(os.path.expanduser("~/.drinks")):
        os.makedirs(os.path.expanduser("~/.drinks"), True)

    # format <timestamp>|<tea_type>|<tea_country>
    with open(filepath, "a") as f:
        f.write(f'{datetime.fromtimestamp(time())}|{tea_type}|{tea_country}\n')

def _key_exists(client, bucket, key):
    """return the key's size if it exist, else None"""
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return obj['Size'] is not None

# TODO break all the s3 stuff into its own module
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


def create_bucket_definition_file(bucket_name, filepath):
    with open(filepath, "w") as f:
        f.write(bucket_name)


def get_or_create_bucket_name(bucket_name=None):
    """
    """
    # persist the name to a local file so we can refer back to it
    filepath = os.path.expanduser("~/.drinks/bucket.txt")

    if bucket_name:
        create_bucket_definition_file(bucket_name, filepath)
        return

    stored_name = None
    if os.path.exists(filepath):
        with open(filepath) as f:
            stored_name = f.readline().strip()

    if stored_name:
        return stored_name
    
    bucket_name = f"caffeine-tracker-{uuid4()}"
    create_bucket_definition_file(bucket_name, filepath)

    return bucket_name


def create_bucket_if_not_exists(bucket_name):
    s3_client = boto3.client('s3')

    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return
    except Exception as e:
        print("Bucket {bucket_name} does not exist. Creating...")
    
    s3_resource = boto3.resource('s3')

    s3_resource.create_bucket(
        ACL="public-read-write",
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
    )


def _s3_persist_file(func, file_name, bucket_name=None):
    directory = os.path.expanduser(f"~/.drinks/")
    filepath = os.path.join(directory, file_name)

    if not os.path.exists(directory):
        os.makedirs(directory, True)

    # TODO genericize this somehow
    bucket = get_or_create_bucket_name(bucket_name)

    create_bucket_if_not_exists(bucket)

    # load file from s3 into temp file
    s3_client = boto3.client('s3')
    if _key_exists(s3_client, bucket, file_name):
        s3_client.download_file(bucket, file_name, filepath)
    else:
        # create the file locally if it doesn't exist in s3
        open(filepath, "a").close()

    # call function with location of file
    func(filepath)

    # copy back into s3
    upload_file(filepath, bucket, file_name)


def main(args):
    if args.type not in ["puerh", "sheng", "shou", "black", "green", "white", "oolong", "herbal", "other"]:
        print(f"Warning: tea type {args.type} not recognized. Should I continue (y/n)?")

        response = sys.stdin.readline().lower().strip()
        if response != "y" and response != "yes":
            print("Exiting")
            sys.exit()

    _s3_persist_file(
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