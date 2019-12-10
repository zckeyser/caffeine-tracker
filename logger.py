import logging
import os


def get_logger(filepath=None):
    logger = logging.getLogger("caffeine-tracker")

    if not filepath:
        userdir = os.path.expanduser("~")
        os.path.join(userdir, ".drinks", "drinks.log")

    fh = logging.FileHandler(filepath)
    fh.setLevel(logging.INFO)

    logger.addHandler(fh)

    return logger

# LOGGER = _get_logger()
