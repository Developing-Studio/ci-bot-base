import discord
import traceback
import sys
from discord.ext import commands

import utils


class ErrorHandler(commands.Cog):
    """Error Handler so your console doesn't get filled with them."""

    def __init__(self, bot):
        self.bot: utils.MyBot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        if hasattr(ctx.command, "on_error"):
            return

        cog = ctx.cog
        if cog:
            # noinspection PyProtectedMember
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f"`{ctx.command}` has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            await ctx.send_help(ctx.command)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"Hey I'm missing these permissions: `{', '.join(error.missing_perms)}`")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"Hey you're missing these permissions: `{', '.join(error.missing_perms)}`",
                delete_after=5.0
            )

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"That command is on cooldown for another `{int(error.retry_after)}` seconds",
                delete_after=5.0
            )

        elif isinstance(error, commands.CheckFailure):
            if ctx.command in self.bot.disabled_commands.keys():
                await ctx.send(f"That command is currently disabled for: {self.bot.disabled_commands[ctx.command]}")

        elif isinstance(error, commands.NotOwner):
            owners = ", ".join([str(self.bot.get_user(owner))
                                for owner in utils.config("BOT_OWNERS")])
            await ctx.send(f"Sorry, you must be: {owners} to use this command.")

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print("Ignoring exception in command {}:".format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
