from copy import deepcopy
from random import randint
from .quotereader import read_quotes
from logging import getLogger

logger = getLogger(__name__)


class QuoteGetter:

    # for the source of truth - the list and the length of the list
    ORIGINAL_DATA = []
    ORIGINAL_DATA_LENGTH = 0

    UP_FOR_RELEASE = []  # pool of quotes that have not been said by the bot
    RELEASED = []  # pool of quotes that have been said by the bot

    def __init__(self):
        # get from source of truth
        self.ORIGINAL_DATA = read_quotes()
        self.ORIGINAL_DATA_LENGTH = len(self.ORIGINAL_DATA)
        # pool for quotes up for release will be independent from the source of truth, thus the hard copy
        self.UP_FOR_RELEASE = deepcopy(self.ORIGINAL_DATA)

    # pooling implementation here
    def get_quote(self):
        # getting the random quote happens here
        random_index_for_release = randint(0, len(self.UP_FOR_RELEASE) - 1)
        quote_released = self.UP_FOR_RELEASE.pop(random_index_for_release)

        # consider adding to the released pool the random quote that was popped
        self.RELEASED.append(quote_released)

        up_for_release_remaining = len(self.UP_FOR_RELEASE)
        released_count = len(self.RELEASED)

        # Logging how many quotes are left per pool
        logger.debug(
            f"Currently {up_for_release_remaining} quote/s remaining to be said..."
        )
        logger.debug(f"Currently {released_count} quote/s said...")

        # logic for resetting pool happens here
        if released_count == self.ORIGINAL_DATA_LENGTH:
            logger.info(
                "All Xander quotes in the repository have been said... Resetting pool..."
            )
            self.UP_FOR_RELEASE = deepcopy(self.RELEASED)
            self.RELEASED.clear()

        logger.info("Successfully got a random Xander quote...")
        return quote_released

    def get_up_for_release_quotes_length(self):
        return len(self.UP_FOR_RELEASE)

    def get_released_quotes_length(self):
        return len(self.RELEASED)
