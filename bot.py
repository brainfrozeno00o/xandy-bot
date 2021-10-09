from discord import Embed, Game
from discord.activity import Activity, Streaming
from discord.enums import ActivityType, Status
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
LOG_MESSAGE_ID = getenv("MESSAGE_ID")

COMMON_SLEEP_TIME = 90  # may be an environment variable but not really

xanderShit = QuoteGetter()  # initializing Quote Getter object

fileConfig("logger.ini", disable_existing_loggers=False)

main_logger = getLogger("__main__")
main_logger.debug(f"Running bot on version {__version__} on {ENVIRONMENT} environment")

intents = Intents.all()

# added initial status first here
bot = commands.Bot(
    command_prefix="xandy",
    intents=intents,
    activity=Game("Dota 2 forever"),
    status=Status.online,
)  # to be used soon when playing specific K-pop songs

GENERAL_CHANNEL_LIST = []
XANDER_BOT_TEST_CHANNEL_LIST = []


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

    # initialize the message_id to 0 first if LOG_MESSAGE_ID is not found in the .env
    message_id = 0 if LOG_MESSAGE_ID == "" else int(LOG_MESSAGE_ID)

    # initialize the message to None if message_id = 0 is not found in the .env
    message = None if message_id == 0 else await logs_channel.fetch_message(message_id)

    while True:
        period = datetime.now(pytz.utc)

        # sending logs every five minutes EXCEPT every hour
        if period.minute % 5 == 0 and period.minute != 0:

            main_logger.info("Sending logs...")

            current_list = (
                XANDER_BOT_TEST_CHANNEL_LIST
                if ENVIRONMENT == "development"
                else GENERAL_CHANNEL_LIST
            )

            guild_list = []

            for channel in current_list:
                guild_list.append(channel.guild.name)

            guild_string = "\n".join(guild_list)

            log_message = f"""
```
Log at this time: {period.now(pytz.timezone("Asia/Singapore")).strftime("%d-%m-%Y %H:%M:%S %z")}

Number of servers currently serving: {len(current_list)}

Number of quotes released: {xanderShit.get_released_quotes_length()}

Number of quotes up for release: {xanderShit.get_up_for_release_quotes_length()}

Server List:
{guild_string}
```
            """

            # check instead if message = None
            if message == None:
                message = await logs_channel.send(
                    content=log_message
                )  # set new message as long as the bot is active
                message_id = message.id
                main_logger.info(f"Log Message ID: {message_id}")
            else:
                await message.edit(content=log_message)

            time = 270  # wait for four minutes and thirty seconds
        else:
            time = 1

        await sleep(time)


async def send_xander_quote():
    await bot.wait_until_ready()

    main_logger.info("Getting channels from all guilds...")

    for channel in bot.get_all_channels():
        if channel.name == "general" and ENVIRONMENT != "development":
            main_logger.info(
                f"Guild name: {channel.guild.name} that has a general channel..."
            )
            GENERAL_CHANNEL_LIST.append(channel)
        elif channel.name == "xander-bot-test-channel" and ENVIRONMENT == "development":
            main_logger.info(
                f"Guild name: {channel.guild.name} that has a xander-bot-test-channel..."
            )
            XANDER_BOT_TEST_CHANNEL_LIST.append(channel)

    while True:
        period = datetime.now(pytz.utc)

        timed_condition = (
            period.minute % 2 == 0  # send at every 2nd minute
            if ENVIRONMENT == "development"
            else period.hour == 0 and period.minute == 0  # send at 8:00 AM UTC+8
        )

        channel_list = (
            XANDER_BOT_TEST_CHANNEL_LIST
            if ENVIRONMENT == "development"
            else GENERAL_CHANNEL_LIST
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

            for channel in channel_list:
                await channel.send(content=message, embed=xander_embed)

            time = COMMON_SLEEP_TIME
        else:
            time = 1

        await sleep(time)


async def change_status():
    await bot.wait_until_ready()

    main_logger.info("Task for determining status has now started...")

    while True:
        period = datetime.now(pytz.utc)

        # only set the statuses at the exact time
        if period.second == 0:
            # currently no switch case in Python... will go with the basic implementation first
            # set once it is 8 am
            if period.hour == 0 and period.minute == 0:
                await bot.change_presence(
                    activity=Game(name="Dota 2 forever"), status=Status.online
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 9 pm
            elif period.hour == 13 and period.minute == 0:
                await bot.change_presence(
                    activity=Streaming(
                        name="Sexercise", url="https://www.twitch.tv/kiaraakitty"
                    ),
                    status=Status.dnd,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 10:45 pm
            elif period.hour == 14 and period.minute == 45:
                await bot.change_presence(
                    activity=Game(name="with myself in the shower"), status=Status.dnd
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 10:55 pm
            elif period.hour == 14 and period.minute == 55:
                await bot.change_presence(
                    activity=Game(name="with my milk and steamed bananas"),
                    status=Status.dnd,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 11 pm
            elif period.hour == 15 and period.minute == 0:
                await bot.change_presence(
                    activity=Game(
                        "with people that do not think that Yoimiya is the best"
                    ),
                    status=Status.online,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 1 am
            elif period.hour == 17 and period.minute == 0:
                await bot.change_presence(
                    activity=Activity(
                        type=ActivityType.watching, name="K-pop idols/trainees cry"
                    ),
                    status=Status.dnd,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 2 am
            elif period.hour == 18 and period.minute == 0:
                await bot.change_presence(
                    activity=Game("with Albdog <3"), status=Status.dnd
                )
                time = COMMON_SLEEP_TIME
            else:
                time = 1
        else:
            time = 1
        await sleep(time)


bot.loop.create_task(send_xander_quote())
bot.loop.create_task(send_logs())
bot.loop.create_task(change_status())

bot.run(TOKEN)
