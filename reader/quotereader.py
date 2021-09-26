from importlib.resources import open_text
from json import load
from sys import path
from logging import getLogger

# add parent package
path.insert(0, "..")

logger = getLogger(__name__)


def read_quotes():
    with open_text("data", "xander-quotes.json") as file:
        logger.info("Opening JSON file for reading...")
        data = load(file)

    logger.info("Done reading JSON file and returning read quotes...")
    # get the value xanderQuotes of key
    return data["xanderQuotes"]
