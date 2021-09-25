from importlib.resources import open_text
from json import load
from sys import path
from logging import getLogger

path.insert(0, "..")  # add parent package

logger = getLogger(__name__)


def read_quotes():
    with open_text("data", "sample-quotes.json") as file:
        logger.info("Opening JSON file for reading...")
        data = load(file)

    logger.info("Done reading JSON file and returning read quotes...")
    return data["xanderQuotes"]  # get the value xanderQuotes key


# print(read_quotes())
