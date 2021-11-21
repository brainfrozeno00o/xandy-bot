from discord import Embed, Game
from discord.activity import Activity, Streaming
from discord.colour import Colour
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.errors import Forbidden
from discord.ext.commands.errors import CommandNotFound
from discord.flags import Intents
from reader.quote_getter import QuoteGetter
from dotenv import load_dotenv
from logging import getLogger
from logging.config import fileConfig
from os import getenv
from sys import exit
from datetime import datetime
from asyncio import sleep
from alembic.config import Config
from alembic import command

import pytz
import signal

load_dotenv()

__version__ = "1.2.0"

# ALL STRINGS, CONVERT TO INT WHEN NEEDED
TOKEN = getenv("DISCORD_TOKEN")
IMAGE = getenv("XANDER_IMAGE")
IMAGE_2 = getenv("XANDER_IMAGE_2")
ENVIRONMENT = getenv("ENVIRONMENT")
LOGS_CHANNEL_ID = getenv("XANDY_LOG_CHANNEL_ID")
LOG_MESSAGE_ID = getenv("MESSAGE_ID")
BLITZ_ID = getenv("KRAZY_ID")  # id of the user bot has to listen to
BLITZ_TIMEOUT = getenv(
    "KRAZY_TIMEOUT"
)  # number of seconds to wait after bot sends the mention
COMMON_SLEEP_TIME = int(
    getenv("COMMON_SLEEP_TIME")
)  # now has become an environment variable due to development changes

# set up variables
DELETE_AFTER_SECONDS = 10  # only using this option when in development
TIMER_ON = False  # initially default to false when booting the bot

xanderShit = None

fileConfig("logger.ini", disable_existing_loggers=False)

main_logger = getLogger("__main__")
main_logger.debug(f"Running bot on version {__version__} on {ENVIRONMENT} environment")

# for running the migration scripts
main_logger.info("Running migration scripts...")
alembic_config = Config("./alembic.ini")
command.upgrade(alembic_config, "head")

intents = Intents.all()

# get all the cogs
extensions = ["cogs.helpx3", "cogs.xandy"]

# added initial status first here
bot = commands.Bot(
    command_prefix="%",
    intents=intents,
    activity=Game("Dota 2 forever | %helphelphelp"),
    help_command=None,  # disabling default help command due to custom help command
    status=Status.online,
)

GENERAL_CHANNEL_LIST = []
XANDER_BOT_TEST_CHANNEL_LIST = []

# helper method for sending the embed on the channel where the invalid commmand is called
async def send_embed(ctx, embed):
    """
    Basically this is the helper function that sends the embed that is only for this class/cog
    Takes the context and embed to be sent to the channel in this following hierarchy
    - tries to send the embed in the channel
    - tries to send a normal message when it cannot send the embed
    - tries to send embed privately with information about the missing permissions
    """
    main_logger.info("Sending embed...")

    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send(
                "Why can't I send embeds?!?!?!? Please check my permissions. PLEEEASEEEEE."
            )
        except:
            await ctx.author.send(
                f"I cannot send the embed in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform Anjer Castillo on this. :slight_smile: ",
                embed=embed,
            )


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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        main_logger.error(
            f"Error occurred since no command was found. Called by {ctx.author}"
        )
        # generate embed for no error
        no_command_emb = Embed(
            title="Currently not a command :slight_frown:",
            description="In case you want that to be a command, please talk to the REAL Xander Castillo. :smile:",
            color=Colour.red(),
        )
        await send_embed(ctx, no_command_emb)
        return
    raise error


@bot.event
async def on_message(message):
    # important to put when processing commands first
    await bot.process_commands(message)

    global TIMER_ON  # had to force this
    if message.author.id == int(BLITZ_ID):  # need to cast to int
        if TIMER_ON == True:
            main_logger.info("Currently waiting for timer to end...")
            return
        else:
            TIMER_ON = True
            try:
                await message.channel.send(f"HOY {message.author.mention}")
                main_logger.info("Successfully sent the callout...")
                t = int(BLITZ_TIMEOUT)  # number of seconds
                while t > 0:
                    await sleep(1)
                    t -= 1
                TIMER_ON = False
            except Exception as e:
                main_logger.error(
                    f"Error when trying to send the callout to {message.author.name} in {message.channel}: {e}"
                )
                TIMER_ON = False
                pass
    else:
        return


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

        try:
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

Number of quotes released in current runtime: {xanderShit.get_released_quotes_length()}

Number of quotes up for release in current runtime: {xanderShit.get_up_for_release_quotes_length()}

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
        # catching any exception for now, and print error and then restart the task
        except Exception as e:
            main_logger.error(f"Error occurred at sending logs task: {e}")
            pass


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

        try:

            timed_condition = (
                period.minute % 10
                != 0  # send at every minute except at every 10th minute
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
                    # remove it to avoid clogging the test channels
                    if ENVIRONMENT == "development":
                        await channel.send(
                            content=message,
                            embed=xander_embed,
                            delete_after=DELETE_AFTER_SECONDS,
                        )
                    else:
                        await channel.send(
                            content=message,
                            embed=xander_embed,
                        )

                # store the quote after sending the embed
                xanderShit.store_inserted_quote(xander_quote)
                time = COMMON_SLEEP_TIME
            else:
                time = 1

            await sleep(time)
        # catching any exception for now, and print error and then restart the task
        except Exception as e:
            main_logger.error(f"Error occurred at sending quotes task: {e}")
            pass


async def change_status():
    await bot.wait_until_ready()

    main_logger.info("Task for determining status has now started...")

    while True:
        period = datetime.now(pytz.utc)

        try:
            # currently no switch case in Python... will go with the basic implementation first
            # set once it is 8 am
            if period.hour == 0 and period.minute == 0:
                await bot.change_presence(
                    activity=Game(name="Dota 2 forever | %helphelphelp"),
                    status=Status.online,
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
                    activity=Game(name="with myself in the shower | %helphelphelp"),
                    status=Status.dnd,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 10:55 pm
            elif period.hour == 14 and period.minute == 55:
                await bot.change_presence(
                    activity=Game(
                        name="with my milk and steamed bananas | %helphelphelp"
                    ),
                    status=Status.dnd,
                )
                time = COMMON_SLEEP_TIME
            # set once it is at 11 pm
            elif period.hour == 15 and period.minute == 0:
                await bot.change_presence(
                    activity=Game(
                        "with people that do not think that Yoimiya is the best | %helphelphelp"
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
                    activity=Game("with Albdog <3 | %helphelphelp"), status=Status.dnd
                )
                time = COMMON_SLEEP_TIME
            else:
                time = 1

            await sleep(time)
        # catching any exception for now, and print error and then restart the task
        except Exception as e:
            main_logger.error(f"Error occurred at changing status task: {e}")
            pass


bot.loop.create_task(send_xander_quote())
bot.loop.create_task(send_logs())
bot.loop.create_task(change_status())


def terminateProcess(signalNumber, frame):
    try:
        xanderShit.store_quotes_up_for_release()
    except (Exception) as error:
        main_logger.error(
            f"Tried storing quotes up for release but an error occurred: {error}"
        )
    finally:
        xanderShit.close_connection()
        exit()


# load the cogs here, initialize the Quote Getter object and handling the terminate signals as well
if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension(extension)

    xanderShit = QuoteGetter()
    bot.all_quotes = xanderShit.get_all_quotes()
    bot.quote_image = IMAGE_2
    bot.all_images = xanderShit.get_all_images()

    # handling terminations here for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, terminateProcess)
    signal.signal(signal.SIGTERM, terminateProcess)


xanderShit.get_connection_info()
bot.run(TOKEN)
