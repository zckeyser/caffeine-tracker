"""
Module for s3 helpers, particularly around downloading, changing then re-uploading a file
"""
import os
from uuid import uuid4

import boto3

from logger import get_logger
LOGGER = get_logger()

# TODO private methods where appropriate


def key_exists(client, bucket, key):
    """return the key's size if it exist, else None"""
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return obj['Size'] is not None


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
    s3_client = boto3.client("s3", region_name="us-east-2")
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

    s3_resource = boto3.resource('s3', region_name='us-east-2')

    s3_resource.create_bucket(
        ACL="public-read-write",
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
    )


def s3_persist_file(func, file_name, bucket_name=None):
    directory = os.path.expanduser(f"~/.drinks/")
    filepath = os.path.join(directory, file_name)

    if not os.path.exists(directory):
        os.makedirs(directory, True)

    bucket = get_or_create_bucket_name(bucket_name)

    create_bucket_if_not_exists(bucket)

    # load file from s3 into temp file
    s3_client = boto3.client('s3')
    if key_exists(s3_client, bucket, file_name):
        s3_client.download_file(bucket, file_name, filepath)
    else:
        # create the file locally if it doesn't exist in s3
        open(filepath, "a").close()

    LOGGER.debug(f"Loaded file from s3://{bucket}/{file_name} to {filepath}")

    # call function with location of file
    func(filepath)

    # copy back into s3
    upload_file(filepath, bucket, file_name)
