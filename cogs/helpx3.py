import discord
from discord.ext import commands
from discord.errors import Forbidden
from logging import getLogger

"""
This implementation of the custom of the help command for the XandyBot is from the gist below:
https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2

There are some slight modifications made due to how we want this specific command to be used.
"""

logger = getLogger(__name__)

# helper method for sending the embed on the channel where the help commmand is called
async def send_embed(ctx, embed):
    """
    Basically this is the helper function that sends the embed message: only for this class/cog
    Takes the context and embed to be sent to the channel in this following hierarchy
    - tries to send the embed in the channel
    - tries to send a normal message when it cannot send the embed
    - tries to send embed privately with information about the missing permissions
    """
    logger.info("Sending embed...")

    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send(
                "Why cannot I send embeds?!?!?!?. Please check my permissions. PLEEEASEEEEE."
            )
        except:
            await ctx.author.send(
                f"I cannot send the embed in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform Anjer Castillo on this. :slight_smile: ",
                embed=embed,
            )


class Help(commands.Cog):

    COMMANDS_LIST = []
    MILK_EMOJI = "<:milk:898924723658948680>"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="helphelphelp",
        aliases=["help", "helpx3"],
        help="HEEELP HEEELP HEEELP!!!",
        description="XandyBot here at your service :heart:",
    )
    async def helphelphelp(self, ctx, *input):
        logger.debug("A user called help!")

        try:
            # get all commands from all cogs
            for cog in self.bot.cogs:
                for command in self.bot.get_cog(cog).get_commands():
                    self.COMMANDS_LIST.append(command)

            # check if there is an input, if not get all the available commands
            if not input:
                logger.info("Asked for general help...")
                # building the embed Object
                help_emb = discord.Embed(
                    title="XandyBot commands",
                    color=discord.Color.dark_gold(),
                    description="So you are asking for my help? Well, here comes the help.\n",
                )

                # iterate through all the list of commands and get their respective descriptions
                for command in self.COMMANDS_LIST:
                    help_emb.add_field(
                        name=command.name,
                        value=f"{self.MILK_EMOJI} {command.description}",
                        inline=False,
                    )

            # call this if they give a specific command or alias
            elif len(input) == 1:
                logger.info("Asked help for one command or alias...")
                # iterate through the commands
                for command in self.COMMANDS_LIST:
                    if (
                        command.name.lower() == input[0].strip().lower()
                        or input[0].strip().lower() in command.aliases
                    ):
                        # generate a different embed message
                        help_emb = discord.Embed(
                            title=f"HEEELP for {input[0]}", color=discord.Color.gold()
                        )
                        help_emb.add_field(
                            name="Description",
                            value=f"{command.description}",
                            inline=False,
                        )
                        help_emb.add_field(
                            name="Help Text", value=f"{command.help}", inline=False
                        )
                        help_emb.add_field(
                            name="Aliases",
                            value=f'{",".join(command.aliases)}',
                            inline=False,
                        )

                        break
                # called when no break was called... interesting Python
                else:
                    help_emb = discord.Embed(
                        title="WTF did you just do?!?!?!",
                        description=f"What is this command: {input[0]}. Why was I not informed?!?!",
                        color=discord.Color.orange(),
                    )
            # call if more than 1 command
            elif len(input) > 1:
                logger.error("Asked help for more than one command...")
                # admit that the bot cannot handle it
                help_emb = discord.Embed(
                    title="That's too much for me to handle. I admit defeat.",
                    description="Please request only one command at a time. :sweat_smile:",
                    color=discord.Color.orange(),
                )
            else:
                logger.error("Something fishy happened...")
                help_emb = discord.Embed(
                    title="YOU HAVE SUCCESSFULLY DESTROYED XANDYBOT! HOW DO YOU FUCKING FEEEEEEL",
                    description="Okay I am panicking. Please contact THE REAL Xander Castillo if this shit happens. Thank you. I love you. You are a great human being.",
                    color=discord.Color.red(),
                )

            # set footer that this bot is powered by Xander's money
            help_emb.set_footer(text="This bot is powered by Xander's money")
            # clear the commands list to avoid repeating it when help is called again
            self.COMMANDS_LIST.clear()
            # send the embed with the helper function
            await send_embed(ctx, help_emb)
        except Exception as e:
            logger.error(f"Error occurred when trying to call help command: {e}")
            pass


def setup(bot):
    bot.add_cog(Help(bot))
