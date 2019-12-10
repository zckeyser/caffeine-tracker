import os
import sys

from logger import get_logger

LOGGER = get_logger("test.log")


if __name__ == "__main__":
    LOGGER.debug("My first log!")
    print(LOGGER.handlers[0].level)

    if not os.path.exists("test.log"):
        print("Log file doesn't exist")
        sys.exit()

    with open("test.log") as f:
        line = f.readline()

        print(line)

    os.remove("test.log")
