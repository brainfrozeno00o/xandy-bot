from discord import Embed
from discord.ext import commands
from reader.quotegetter import QuoteGetter
from dotenv import load_dotenv
from logging import getLogger
from logging.config import fileConfig
from os import getenv
from datetime import datetime
from asyncio import sleep

import pytz

load_dotenv()

__version__ = "1.0.0"

TOKEN = getenv("DISCORD_TOKEN")
IMAGE = getenv("XANDER_IMAGE")
ENVIRONMENT = getenv("ENVIRONMENT")

xanderShit = QuoteGetter()  # initializing Quote Getter object

fileConfig("logger.ini", disable_existing_loggers=False)

main_logger = getLogger("__main__")
main_logger.debug(f"Running bot on version {__version__} on {ENVIRONMENT} environment")

bot = commands.Bot(
    command_prefix="xandy"
)  # to be used soon when playing specific K-pop songs


@bot.event
async def on_ready():
    main_logger.info("Bot now ready...")


async def send_xander_quote():
    await bot.wait_until_ready()

    main_logger.info("Getting channels from all guilds...")

    all_channels = bot.get_all_channels()
    general_channel_list = []

    for channel in all_channels:
        if channel.name == "general":
            main_logger.info("Bot has now found channel to send message...")
            # general_channel = channel
            general_channel_list.append(channel)

    while not bot.is_closed():
        period = datetime.now(pytz.utc)

        timed_condition = (
            period.minute % 2 == 0  # send at every 2nd minute
            if ENVIRONMENT == "development"
            else period.hour == 0 and period.minute == 0  # send at 8:00 AM UTC+8
        )

        if timed_condition:
            xander_quote = xanderShit.get_quote()

            main_logger.info("Generating embed for sending...")

            quote_taken = xander_quote["quote"]
            context_taken = xander_quote["context"]

            # quotes with the new line most likely have the quotation marks already within the quote
            if "\n" in quote_taken:
                embed_description = f"""
                    {quote_taken}
                    - {context_taken}
                """
            else:
                embed_description = f'"{quote_taken}" - {context_taken}'

            xander_embed = Embed(
                title="Xander Quote of the Day",
                description=embed_description,
                color=0xCF37CA,
            )
            xander_embed.set_footer(text="This bot is powered by Xander's money")
            xander_embed.set_image(url=IMAGE)
            main_logger.info(
                "Bot now sending embed message with content in all general channels..."
            )

            message = "Hello @everyone!"

            for channel in general_channel_list:
                await channel.send(content=message, embed=xander_embed)
            time = 90
        else:
            time = 1
        await sleep(time)


bot.loop.create_task(send_xander_quote())

bot.run(TOKEN)
