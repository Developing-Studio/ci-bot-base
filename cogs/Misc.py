from discord.ext import commands

import utils


class Misc(commands.Cog, name="Miscellaneous"):
    """All the miscellaneous commands"""

    def __init__(self, bot):
        self.bot: utils.MyBot = bot

    @commands.Cog.listener("on_command")
    async def chunk_on_cmd(self, ctx: commands.Context):
        """An event to chunk a guild as soon as they run a cmd for the first time."""

        if ctx.guild and not ctx.guild.chunked:
            await ctx.guild.chunk()

    @commands.command()
    async def hello(self, ctx):
        """Gives the author the bots introduction."""

        owners = ", ".join([str(self.bot.get_user(owner))
                            for owner in utils.config("BOT_OWNERS")])
        await ctx.send(
            f"Hello {ctx.author} my name is {self.bot.user.name} created by {owners} with the reasoning of: "
            f"{self.bot.description}"
        )


def setup(bot):
    bot.add_cog(Misc(bot))
