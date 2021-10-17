from random import randint
from discord import Embed
from discord.ext import commands
from discord.errors import Forbidden
from logging import getLogger

logger = getLogger(__name__)

# helper method for sending the embed on the channel where the commmand is called
async def send_embed(ctx, embed):
    """
    Basically this is the helper function that sends the embed that is only for this class/cog
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
                "Why can't I send embeds?!?!?!? Please check my permissions. PLEEEASEEEEE."
            )
        except:
            await ctx.author.send(
                f"I cannot send the embed in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform Anjer Castillo on this. :slight_smile: ",
                embed=embed,
            )


class Xandy(commands.Cog):

    # yes answers
    AFFIRMATIVE = ["LGTM", "Looks good to me!", "Parfait!", "Nice"]

    # no answers
    NEGATIVE = [
        "Hell nah!",
        "Gawa mo ba 'yan? Kasi ang panget!!!",
        "We know what we do not know.",
    ]

    # unsure answers
    UNSURE = [
        "Tanong mo sa mama mo",
        "Hindi ko alam. Hindi ko naman task 'yan eh.",
        "Huwag mo akong tanungin. Malungkot pa ako. :cry:",
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="lgtm",
        aliases=["okba", "pwedeba"],
        help="%lgtm <question|statement>",
        description="I will try my best to say something on what you say :sweat_smile:",
    )
    async def lgtm(self, ctx, *input):
        logger.debug("Someone wants to know what the bot has to say...")

        try:
            # check if there is no input
            if not input:
                logger.info("Call command for what...")
                # generate embed for no question/statement
                answer_embed = Embed(title="?", color=0xCF37CA)
            # to be called when there is input
            else:
                logger.info("Generating response...")
                """
                Determining what the answer would be using integers, the value will be as follows:
                0 = YES
                1 = NO
                2 = UNSURE
                """
                answer_int = randint(0, 2)

                # bad if-else incoming
                if answer_int == 0:
                    answer_list = self.AFFIRMATIVE
                elif answer_int == 1:
                    answer_list = self.NEGATIVE
                else:
                    answer_list = self.UNSURE

                # getting random answer
                answer_index = randint(0, len(answer_list) - 1)
                answer = answer_list[answer_index]

                # generate the embed
                answer_embed = Embed(
                    title=f"{' '.join(input)}", description=f"{answer}", color=0xCF37CA
                )
            # set footer that this bot is powered by Xander's money
            answer_embed.set_footer(text="This bot is powered by Xander's money")
            # send the embed using the helper function
            await send_embed(ctx, answer_embed)
        except Exception as e:
            logger.error(f"Error occurred when trying to call lgtm command: {e}")
            pass


def setup(bot):
    bot.add_cog(Xandy(bot))
