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

# helper method for sending a message with an image
async def send_message_with_image(ctx, message, image):
    """
    Basically this is the helper function that sends the message with an image that is only for this class/cog
    Takes the context, message, and image to be sent to the channel in this following hierarchy
    - tries to send the message and image in the channel
    - tries to send a normal message when it cannot send both message and image
    - tries to send message and image privately with information about the missing permissions
    """
    logger.info("Sending message with image...")

    try:
        await ctx.send(message)
        await ctx.send(image)
    except Forbidden:
        try:
            await ctx.send(
                "Why can't I send a message with an image?!?!?!? Please check my permissions. PLEEEASEEEEE."
            )
        except:
            await ctx.author.send(
                f"I cannot send this message: {message} with a image in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform Anjer Castillo on this. :slight_smile: ",
            )
            await ctx.author.send(image)

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
        name="pogi",
        aliases=["image", "xandypic"],
        help="%pogi",
        description="I will send a picture of my sexy self."
    )
    async def pogi(self, ctx):
        logger.debug("Someone wants to request a Xander image...")

        try:
            all_images = self.bot.all_images
            all_images_length = len(all_images)

            # get random image
            random_index = randint(0, all_images_length - 1)
            random_image = all_images[random_index]
            image_link = random_image[1]

            # process message
            message = "Here is a handsome picture of me. Hope you enjoy. :kissing_heart:"

            # send the message
            await send_message_with_image(ctx, message, image_link)
        except Exception as e:
            logger.error(f"Error occurred when trying to call pogi command: {e}")
            pass
        finally:
            logger.info("Done processing for pogi command...")


    @commands.command(
        name="clown",
        aliases=["quote", "xandysays"],
        help="%clown",
        description="I will give you a random quote at your will. :smile:",
    )
    async def clown(self, ctx):
        logger.debug("Someone wants to request a Xander quote...")

        try:
            # set the variables
            all_quotes = self.bot.all_quotes
            all_quotes_length = len(all_quotes)
            xander_image = self.bot.quote_image

            # getting the random quote
            random_index = randint(0, all_quotes_length - 1)
            random_quote = all_quotes[random_index]

            logger.info("Generating embed for sending...")

            quote_taken = random_quote[1]
            context_taken = random_quote[2]

            # quotes with the new line most likely have the quotation marks already within the quote
            if "\n" in quote_taken:
                embed_description = f"""
                    {quote_taken}
                    - {context_taken}
                """
            else:
                embed_description = f'"{quote_taken}" - {context_taken}'

            # setting up the embed
            xander_embed = Embed(
                title="Random Xander Quote",
                description=embed_description,
                color=0xCF37CA,
            )
            xander_embed.set_footer(text="This bot is powered by Xander's money")
            xander_embed.set_image(url=xander_image)

            logger.info("Sending random quote at will...")
            # send the embed using the helper function
            await send_embed(ctx, xander_embed)
        except Exception as e:
            logger.error(f"Error occurred when trying to call clown command: {e}")
            pass
        finally:
            logger.info("Done processing for clown command...")

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
        finally:
            logger.info("Done processing for lgtm command...")


def setup(bot):
    bot.add_cog(Xandy(bot))
