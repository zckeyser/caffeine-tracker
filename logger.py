"""
Provides a centralized logger definition
"""
import logging
import os

# TODO log with timestamp


def get_logger(filepath=None):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if not filepath:
        userdir = os.path.expanduser("~")
        os.path.join(userdir, ".drinks", "drinks.log")

    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.DEBUG)

    logger.addHandler(fh)

    return logger
