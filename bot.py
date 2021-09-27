from discord import Embed
from discord.ext import commands
from discord.flags import Intents
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
LOGS_CHANNEL_ID = getenv("XANDY_LOG_CHANNEL_ID")

xanderShit = QuoteGetter()  # initializing Quote Getter object

fileConfig("logger.ini", disable_existing_loggers=False)

main_logger = getLogger("__main__")
main_logger.debug(f"Running bot on version {__version__} on {ENVIRONMENT} environment")

intents = Intents.all()

bot = commands.Bot(
    command_prefix="xandy", intents=intents
)  # to be used soon when playing specific K-pop songs

GENERAL_CHANNEL_LIST = []


@bot.event
async def on_ready():
    main_logger.info("Bot now ready...")


@bot.event
async def on_guild_join(guild):
    main_logger.info(f"XandyBot has joined {guild.name}")

    for channel in guild.channels:
        if channel.name == "general":
            main_logger.info(f"Found the general channel in {guild.name}...")
            GENERAL_CHANNEL_LIST.append(channel)
            main_logger.info("Adding another general channel to the list...")


@bot.event
async def on_guild_remove(guild):
    main_logger.info(f"XandyBot has been removed from {guild.name}")

    for channel in GENERAL_CHANNEL_LIST:
        if channel.guild.name == guild.name:
            main_logger.debug(
                f"Removing this general channel from {guild.name} from the list..."
            )
            GENERAL_CHANNEL_LIST.remove(channel)
            main_logger.info("Successfully removed channel...")


async def send_logs():
    await bot.wait_until_ready()

    main_logger.info("Getting log channel in support server...")

    logs_channel = bot.get_channel(int(LOGS_CHANNEL_ID))

    while not bot.is_closed():
        period = datetime.now(pytz.utc)

        # sending logs every three minutes
        if period.minute % 3 == 0:

            main_logger.info("Sending logs...")

            guild_list = []

            for channel in GENERAL_CHANNEL_LIST:
                guild_list.append(channel.guild.name)

            guild_string = "\n".join(guild_list)

            log_message = f"""
```
Log at this time: {period.now(pytz.timezone("Asia/Singapore")).strftime("%d-%m-%Y %H:%M:%S %z")}

Number of servers currently serving: {len(GENERAL_CHANNEL_LIST)}

Number of quotes released: {xanderShit.get_released_quotes_length()}

Number of quotes up for release: {xanderShit.get_up_for_release_quotes_length()}

Server List:
{guild_string}
```
            """

            await logs_channel.send(content=log_message)
            time = 90
        else:
            time = 1
        await sleep(time)


async def send_xander_quote():
    await bot.wait_until_ready()

    main_logger.info("Getting channels from all guilds...")

    for channel in bot.get_all_channels():
        if channel.name == "general":
            main_logger.info(
                f"Guild name: {channel.guild.name} that has a general channel..."
            )
            GENERAL_CHANNEL_LIST.append(channel)

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

            for channel in GENERAL_CHANNEL_LIST:
                await channel.send(content=message, embed=xander_embed)
            time = 90
        else:
            time = 1
        await sleep(time)


bot.loop.create_task(send_xander_quote())
bot.loop.create_task(send_logs())

bot.run(TOKEN)
