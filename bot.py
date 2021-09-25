import logging, logging.config, os, discord, copy, random

from reader.quotereader import read_quotes

from dotenv import load_dotenv

load_dotenv()

__version__ = "1.0.0"

TOKEN = os.getenv("DISCORD_TOKEN")

logging.config.fileConfig("logger.ini", disable_existing_loggers=False)

main_logger = logging.getLogger("__main__")

data = read_quotes()

original_data_length = len(data)

up_for_release = copy.deepcopy(data)
released = []

random_index_for_release = random.randint(0, len(up_for_release) - 1)
quote_released = up_for_release.pop(random_index_for_release)
released.append(quote_released)

print(len(up_for_release))
print(len(released))

# print(up_for_release)

# client = discord.Client()


# @client.event
# async def on_ready():
#     main_logger.info("Bot about to run...")
#     main_logger.debug(f"Running bot on version {__version__}")

#     main_logger.info(data)


# client.run(TOKEN)
